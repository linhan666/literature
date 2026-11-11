#!/usr/bin/env python3
"""Opt-in Crossref DOI metadata comparison (network required).

Crossref identity similarity is NOT claim verification. This tool does not
modify records.csv or promote any verification status automatically.
"""
from __future__ import annotations

import argparse
import csv
from difflib import SequenceMatcher
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from reviewkit import read_rows, write_rows, SCHEMAS, norm_title, normalize_doi

RESULT_FIELDS = ['record_id', 'input_doi', 'crossref_doi', 'input_title', 'crossref_title',
                 'input_year', 'crossref_years', 'title_similarity', 'identity_check', 'note']


def get_crossref(doi: str, timeout: float = 12.0) -> dict:
    url = f'https://api.crossref.org/works/{quote(doi, safe="")}'
    req = Request(url, headers={'User-Agent': 'evidence-first-review-writer/1.0 (public-metadata-comparison)',
                                'Accept': 'application/json'})
    with urlopen(req, timeout=timeout) as resp:
        payload = json.load(resp)
    return payload['message']


def compare(row: dict[str, str], record: dict) -> dict[str, str]:
    cross_title = (record.get('title') or [''])[0]
    cross_doi = normalize_doi(record.get('DOI') or '')
    years = set()
    for field in ('published', 'published-online', 'published-print', 'issued', 'created'):
        item = record.get(field, {}) or {}
        parts = item.get('date-parts') or []
        if parts and parts[0] and parts[0][0]:
            years.add(str(parts[0][0]))
    title_similarity = SequenceMatcher(None, norm_title(row['title']), norm_title(cross_title)).ratio() if row['title'] and cross_title else 0
    if not row['title'] or not row['year']:
        status = 'needs_review'
        note = 'Input lacks title or year; DOI resolution alone is insufficient for identity confirmation'
    elif (cross_doi == normalize_doi(row['doi']) and title_similarity >= 0.86 and row['year'] in years):
        status = 'likely_match'
        note = 'Human must inspect source/publisher; this does not validate any claim'
    else:
        status = 'needs_review'
        note = 'DOI/title/year discrepancy or incomplete publisher metadata'
    return {'record_id': row['record_id'], 'input_doi': row['doi'],
            'crossref_doi': cross_doi, 'input_title': row['title'],
            'crossref_title': cross_title, 'input_year': row['year'],
            'crossref_years': ';'.join(sorted(years)),
            'title_similarity': f'{title_similarity:.3f}', 'identity_check': status,
            'note': note}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--max-records', type=int, default=0, help='0 means all records')
    parser.add_argument('--timeout', type=float, default=12.0)
    args = parser.parse_args()
    if args.max_records < 0 or args.timeout <= 0:
        parser.error('--max-records must be >= 0 and --timeout > 0')
    rows = read_rows(Path(args.records), SCHEMAS['records.csv'])
    if args.max_records:
        rows = rows[:args.max_records]
    output = []
    for row in rows:
        doi = normalize_doi(row['doi'])
        if not doi:
            output.append({'record_id': row['record_id'], 'input_doi': '',
                           'identity_check': 'no_doi', 'note': 'Check PMID/publisher manually'})
            continue
        if not re.fullmatch(r'10\.\d{4,9}/\S+', doi):
            output.append({'record_id': row['record_id'], 'input_doi': row['doi'],
                           'identity_check': 'needs_review', 'note': 'DOI format suspicious'})
            continue
        try:
            record = get_crossref(doi, timeout=args.timeout)
            output.append(compare(row, record))
        except HTTPError as e:
            output.append({'record_id': row['record_id'], 'input_doi': row['doi'],
                           'identity_check': 'not_found' if e.code == 404 else 'error',
                           'note': f'HTTP status {e.code}; no verification inferred'})
        except (URLError, TimeoutError, ValueError, KeyError) as e:
            output.append({'record_id': row['record_id'], 'input_doi': row['doi'],
                           'identity_check': 'error', 'note': f'Crossref request or response failed: {type(e).__name__}'})
        time.sleep(0.2)  # polite request pacing; not a replacement for server rate limits
    write_rows(Path(args.out), RESULT_FIELDS, output)
    counts = {key: sum(r['identity_check'] == key for r in output)
              for key in ('likely_match', 'needs_review', 'not_found', 'error', 'no_doi')}
    print(json.dumps({'checked': len(output), 'results': counts, 'output': args.out,
                      'warning': 'Metadata similarity is not verification of scientific claims'}, indent=2))
    return 0 if not counts['error'] else 1


if __name__ == '__main__':
    sys.exit(main())
