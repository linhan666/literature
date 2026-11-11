#!/usr/bin/env python3
"""Opt-in Europe PMC search adapter: public metadata only, standard library.

Makes a real network request if run. Appends discovered records and an honest
search log; NEVER marks a result as full-text read or independently verified.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from reviewkit import SCHEMAS, ReviewError, normalize_doi, read_rows, write_rows

ENDPOINT = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'


def fetch_page(query: str, cursor: str, page_size: int, timeout: float) -> dict:
    params = {'query': query, 'format': 'json', 'resultType': 'core',
              'pageSize': str(page_size), 'cursorMark': cursor}
    req = Request(ENDPOINT + '?' + urlencode(params),
                  headers={'User-Agent': 'evidence-first-review-writer/1.0 (academic search)',
                           'Accept': 'application/json'})
    with urlopen(req, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or 'resultList' not in payload:
        raise ReviewError('Europe PMC response missing resultList; no files changed')
    return payload


def from_result(r: dict, record_id: str, search_id: str) -> dict[str, str]:
    doi = normalize_doi(str(r.get('doi') or ''))
    pmid = str(r.get('pmid') or '')
    source = str(r.get('source') or '')
    source_id = str(r.get('id') or '')
    url = f'https://doi.org/{doi}' if doi else (
        f'https://europepmc.org/article/{source}/{source_id}' if source_id and source else '')
    return {
        'record_id': record_id,
        'study_id': '',  # study equivalence requires intellectual review
        'title': str(r.get('title') or '').strip(),
        'authors': str(r.get('authorString') or '').strip(),
        'year': str(r.get('pubYear') or '').strip(),
        'doi': doi, 'pmid': pmid,
        'source_type': 'preprint' if source == 'PPR' else 'article_or_report',
        'venue': str(r.get('journalTitle') or ''),
        'url': url,
        'source_db': 'Europe PMC',
        'peer_review_status': 'preprint' if source == 'PPR' else 'unknown',
        'access_level': 'abstract' if r.get('abstractText') else 'metadata_only',
        'metadata_status': 'unverified',
        'notes': f'search_id={search_id}; EuropePMC source={source}; source_id={source_id}; retrieval=public_metadata',
    }


def next_id(prefix: str, rows: list[dict], key: str) -> str:
    nums = [int(m.group(1)) for r in rows if (m := re.fullmatch(re.escape(prefix)+r'(\d+)', r.get(key, '')))]
    return f'{prefix}{max(nums, default=0)+1:04d}'


def run(args: argparse.Namespace) -> dict:
    project = Path(args.project).expanduser().resolve()
    records_path, log_path = project / 'records.csv', project / 'search_log.csv'
    records = read_rows(records_path, SCHEMAS['records.csv'])
    log = read_rows(log_path, SCHEMAS['search_log.csv'])
    query_id = next_id('Q', log, 'search_id')
    start = max((int(r['record_id'][1:]) for r in records if re.fullmatch(r'R\d+', r['record_id'])), default=0)
    results = []
    cursor = '*'
    hit_count = None
    seen_cursors = set()
    while len(results) < args.max_results and cursor not in seen_cursors:
        seen_cursors.add(cursor)
        payload = fetch_page(args.query, cursor, min(args.page_size, args.max_results - len(results)), args.timeout)
        if hit_count is None:
            hit_count = payload.get('hitCount')
        batch = (payload.get('resultList') or {}).get('result') or []
        if not isinstance(batch, list):
            raise ReviewError('Europe PMC resultList.result is not a list; no files changed')
        if not batch:
            break
        results.extend(batch[: args.max_results - len(results)])
        next_cursor = str(payload.get('nextCursorMark') or '')
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        if len(results) < args.max_results:
            time.sleep(args.delay)
    new_records = [from_result(r, f'R{start+i+1:04d}', query_id) for i, r in enumerate(results)]
    entry = {
        'search_id': query_id, 'database': 'Europe PMC REST', 'query': args.query,
        'filters': 'As provided in exact query (not auto-expanded)',
        'run_date': date.today().isoformat(), 'sort': 'Europe PMC API default',
        'limit': str(args.max_results), 'retrieved_count': str(len(results)),
        'notes': f'API hitCount={hit_count}; resultType=core; cursor pagination; public metadata only; capped={len(results) >= args.max_results}'
    }
    # Commit only after all pages have been fetched without errors.
    write_rows(records_path, SCHEMAS['records.csv'], records + new_records)
    write_rows(log_path, SCHEMAS['search_log.csv'], log + [entry])
    return {'query_id': query_id, 'retrieved': len(new_records), 'reported_hit_count': hit_count,
            'max_results': args.max_results,
            'warning': 'Search coverage may be truncated; all source claims require separate verification and full-text examination.'}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', required=True)
    p.add_argument('--query', required=True, help='Exact Europe PMC query string (platform-specific syntax)')
    p.add_argument('--max-results', type=int, default=200)
    p.add_argument('--page-size', type=int, default=100)
    p.add_argument('--timeout', type=float, default=15)
    p.add_argument('--delay', type=float, default=0.3)
    a = p.parse_args()
    if not (1 <= a.max_results <= 10000) or not (1 <= a.page_size <= 200) or a.timeout <= 0 or a.delay < 0:
        p.error('max-results: 1–10000; page-size: 1–200; timeout >0; delay >=0')
    try:
        print(json.dumps(run(a), indent=2, ensure_ascii=False))
        return 0
    except (ReviewError, OSError, HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        print(f'ERROR: Europe PMC search incomplete; no successful search log created: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
