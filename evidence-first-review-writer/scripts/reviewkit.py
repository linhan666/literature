#!/usr/bin/env python3
"""Offline, dependency-free review workspace and integrity checks.

This utility checks structural data consistency, not the scientific correctness
of articles or whether an argument is supported by the full text.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
from datetime import date
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SCHEMAS = {
    'records.csv': ['record_id', 'study_id', 'title', 'authors', 'year', 'doi', 'pmid',
                    'source_type', 'venue', 'url', 'source_db', 'peer_review_status',
                    'access_level', 'metadata_status', 'notes'],
    'search_log.csv': ['search_id', 'database', 'query', 'filters', 'run_date', 'sort',
                       'limit', 'retrieved_count', 'notes'],
    'screening.csv': ['record_id', 'title_abstract_decision', 'full_text_decision',
                       'exclusion_reason', 'reviewer', 'notes'],
    'evidence.csv': ['evidence_id', 'record_id', 'study_id', 'claim_id',
                     'section_or_page', 'evidence_type', 'task', 'dataset',
                     'model_or_method', 'comparator', 'metric', 'metric_value',
                     'split', 'uncertainty', 'limitations', 'quote_or_paraphrase',
                     'support_status'],
    'claims.csv': ['claim_id', 'claim_text', 'claim_type', 'strength',
                   'evidence_ids', 'verdict', 'limitations', 'manuscript_section'],
}

VALID = {
    'metadata_status': {'unverified', 'verified', 'mismatch', 'unavailable'},
    'access_level': {'full_text', 'abstract', 'metadata_only', 'unavailable'},
    'peer_review_status': {'peer_reviewed', 'preprint', 'unknown', 'not_applicable'},
    'title_abstract_decision': {'include', 'exclude', 'pending'},
    'full_text_decision': {'include', 'exclude', 'not_retrieved', 'pending', 'not_applicable'},
    'support_status': {'supports', 'partial', 'contradicts', 'unknown'},
    'verdict': {'supported', 'qualified', 'contested', 'unsupported', 'unreviewed'},
}


class ReviewError(Exception):
    pass


def read_rows(path: Path, fields: list[str] | None = None) -> list[dict[str, str]]:
    if not path.exists():
        raise ReviewError(f'File does not exist: {path}')
    with path.open('r', encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ReviewError(f'CSV missing header: {path}')
        if fields is not None:
            absent = [k for k in fields if k not in reader.fieldnames]
            if absent:
                raise ReviewError(f'{path.name} missing required columns: {absent}')
        output = []
        for i, row in enumerate(reader, 2):
            if None in row:
                raise ReviewError(f'{path.name}:{i} has too many columns; quote commas inside fields')
            clean = {k: (v or '').strip() for k, v in row.items()}
            if any(clean.values()):
                output.append(clean)
        return output


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def cli_init(args: argparse.Namespace) -> int:
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    created = []
    for fname, fields in SCHEMAS.items():
        dest = out / fname
        if dest.exists():
            print(f'Skipping existing {dest}')
        else:
            write_rows(dest, fields, [])
            created.append(str(dest))
    for name in ('review_brief.md', 'manuscript.md'):
        dest = out / name
        if dest.exists():
            continue
        source = (ASSETS / name).read_text(encoding='utf-8')
        source = source.replace('{{TOPIC}}', args.topic)
        source = source.replace('{{REVIEW_TYPE}}', args.type)
        source = source.replace('{{DATE}}', date.today().isoformat())
        dest.write_text(source, encoding='utf-8')
        created.append(str(dest))
    print(json.dumps({'project': str(out), 'created': created,
                      'warning': 'Empty research packet: no search or verification was performed.'},
                     indent=2, ensure_ascii=False))
    return 0


def normalize_doi(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', s)
    s = re.sub(r'^doi:\s*', '', s)
    return s.strip().rstrip('.,;')


def norm_title(t: str) -> str:
    t = unicodedata.normalize('NFKD', t).casefold()
    return ''.join(c for c in t if c.isalnum())


def cli_dedupe(args: argparse.Namespace) -> int:
    inp = Path(args.input).expanduser().resolve()
    rows = read_rows(inp, SCHEMAS['records.csv'])
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    ids = [r['record_id'] for r in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ReviewError('Every record must have a unique nonempty record_id before deduplication')
    parent = list(range(len(rows)))
    doi_sets = [{normalize_doi(r['doi'])} - {''} for r in rows]
    pmid_sets = [{r['pmid']} - {''} for r in rows]
    reasons = defaultdict(set)
    conflicts = []

    def root(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int, why: str) -> None:
        a, b = root(a), root(b)
        if a == b:
            reasons[a].add(why)
            return
        if len(doi_sets[a] | doi_sets[b]) > 1 or len(pmid_sets[a] | pmid_sets[b]) > 1:
            conflicts.append({'record_id_a': rows[a]['record_id'],
                              'record_id_b': rows[b]['record_id'],
                              'reason': 'conflicting DOI or PMID despite shared alternate identity'})
            return
        parent[b] = a
        doi_sets[a] |= doi_sets[b]
        pmid_sets[a] |= pmid_sets[b]
        reasons[a] |= reasons[b] | {why}

    keys: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        if normalize_doi(r['doi']):
            keys[('doi', normalize_doi(r['doi']))].append(i)
        if r['pmid']:
            keys[('pmid', r['pmid'])].append(i)
        if r['title'] and r['year']:
            keys[('title-year', norm_title(r['title']) + '|' + r['year'])].append(i)
    for (kind, _), group in sorted(keys.items()):
        for a in range(len(group)):
            for b in range(a + 1, len(group)):
                union(group[a], group[b], kind)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(rows)):
        groups[root(i)].append(i)
    kept = []
    dupmap = []
    for group in groups.values():
        def quality(i: int) -> tuple[int, int]:
            row = rows[i]
            return (sum(bool(row.get(k)) for k in SCHEMAS['records.csv']) +
                    3 * (row['metadata_status'] == 'verified') +
                    2 * (row['access_level'] == 'full_text'), -i)
        winner = max(group, key=quality)
        kept.append(rows[winner])
        for i in group:
            if i != winner:
                dupmap.append({'original_id': rows[i]['record_id'],
                               'canonical_id': rows[winner]['record_id'],
                               'matching_keys': ';'.join(sorted(reasons[root(i)]))})
    kept.sort(key=lambda r: ids.index(r['record_id']))
    write_rows(out / 'deduped_records.csv', SCHEMAS['records.csv'], kept)
    write_rows(out / 'duplicate_map.csv', ['original_id', 'canonical_id', 'matching_keys'], dupmap)
    write_rows(out / 'dedupe_conflicts.csv', ['record_id_a', 'record_id_b', 'reason'], conflicts)
    report = {'input_records': len(rows), 'canonical_records': len(kept),
              'suggested_duplicates': len(dupmap), 'identity_conflicts': len(conflicts),
              'warning': 'Review all suggested merges, metadata conflicts, and source-id references manually.'}
    print(json.dumps(report, indent=2))
    return 0


def cli_audit(args: argparse.Namespace) -> int:
    p = Path(args.project).expanduser().resolve()
    rows = {fname: read_rows(p / fname, fields) for fname, fields in SCHEMAS.items()}
    records = rows['records.csv']
    evidences = rows['evidence.csv']
    claims = rows['claims.csv']
    screenings = rows['screening.csv']
    errors: list[str] = []
    warnings: list[str] = []

    for file, col in [('records.csv', 'record_id'), ('evidence.csv', 'evidence_id'),
                      ('claims.csv', 'claim_id'), ('screening.csv', 'record_id'),
                      ('search_log.csv', 'search_id')]:
        values = [r[col] for r in rows[file]]
        if any(not x for x in values):
            errors.append(f'{file} has empty {col} entries')
        repeats = [k for k, n in Counter(values).items() if n > 1]
        if repeats:
            errors.append(f'{file} duplicates {col}: {repeats[:10]}')

    for file, data in rows.items():
        for row in data:
            identifier = next(iter(row.values()), '(unknown)')
            for key, choices in VALID.items():
                if key in row and row[key] and row[key] not in choices:
                    errors.append(f'{file} {identifier}: invalid {key}={row[key]}')

    record_index = {r['record_id']: r for r in records}
    evidence_index = {r['evidence_id']: r for r in evidences}
    claim_index = {r['claim_id']: r for r in claims}

    for e in evidences:
        rid, eid = e['record_id'], e['evidence_id']
        if rid not in record_index:
            errors.append(f'Evidence {eid} refers to missing record {rid}')
        elif e['study_id'] and record_index[rid]['study_id'] and e['study_id'] != record_index[rid]['study_id']:
            errors.append(f'Evidence {eid}: study_id differs from record {rid}')
        if e['claim_id'] and e['claim_id'] not in claim_index:
            errors.append(f'Evidence {eid}: unknown claim_id {e["claim_id"]}')
        if e['support_status'] == 'supports' and not e['section_or_page']:
            warnings.append(f'Evidence {eid}: support asserted without source locator')
        if rid in record_index and record_index[rid]['access_level'] in ('abstract', 'metadata_only') and e['evidence_type'] == 'primary_fulltext':
            errors.append(f'Evidence {eid}: full-text evidence claimed for non-full-text record {rid}')

    for c in claims:
        cid = c['claim_id']
        linked = [x.strip() for x in c['evidence_ids'].split(';') if x.strip()]
        if c['verdict'] == 'supported' and not linked:
            errors.append(f'Claim {cid}: supported but no evidence_ids')
        for eid in linked:
            if eid not in evidence_index:
                errors.append(f'Claim {cid}: unknown evidence_id {eid}')
            elif evidence_index[eid]['claim_id'] not in ('', cid):
                warnings.append(f'Claim {cid}: evidence {eid} points to different claim {evidence_index[eid]["claim_id"]}')
        if c['verdict'] == 'supported' and any(evidence_index[e]['support_status'] != 'supports' for e in linked if e in evidence_index):
            errors.append(f'Claim {cid}: marked supported despite linked evidence not marked supports')
        if c['verdict'] in ('unsupported', 'unreviewed') and c['claim_text']:
            warnings.append(f'Claim {cid}: {c["verdict"]}; do not present as settled fact')
        if c['strength'] == 'causal' and c['verdict'] == 'supported':
            warnings.append(f'Claim {cid}: causal statement requires expert causal-evidence appraisal')

    for r in records:
        rid = r['record_id']
        if r['doi'] and not re.fullmatch(r'10\.\d{4,9}/\S+', normalize_doi(r['doi'])):
            warnings.append(f'Record {rid}: DOI format unusual; check against publisher')
        if r['metadata_status'] != 'verified':
            warnings.append(f'Record {rid}: metadata status {r["metadata_status"] or "missing"}')
        if r['access_level'] in ('metadata_only', 'abstract'):
            warnings.append(f'Record {rid}: only {r["access_level"]}; limit detailed method claims')
        if r['peer_review_status'] == 'preprint':
            warnings.append(f'Record {rid}: preprint; disclose publication status')
    for s in screenings:
        if s['record_id'] not in record_index:
            errors.append(f'Screening refers to missing record {s["record_id"]}')
        if s['title_abstract_decision'] == 'exclude' and s['full_text_decision'] == 'include':
            errors.append(f'Screening {s["record_id"]}: excluded at title yet included at full text')
        if s['full_text_decision'] == 'exclude' and not s['exclusion_reason']:
            errors.append(f'Screening {s["record_id"]}: full-text exclusion has no reason')

    manuscript = Path(args.manuscript).expanduser().resolve() if args.manuscript else p / 'manuscript.md'
    manuscript_exists = manuscript.exists()
    if manuscript_exists:
        content = manuscript.read_text(encoding='utf-8')
        # draft cite tags: [@R0001] or [@R0001; @R0002]
        cited = set(re.findall(r'@(?P<id>R\d{3,})\b', content))
        for rid in sorted(cited):
            if rid not in record_index:
                errors.append(f'Manuscript cites unknown record {rid}')
            elif record_index[rid]['metadata_status'] != 'verified':
                warnings.append(f'Manuscript cites unverified metadata {rid}')
        linked_claims = set(re.findall(r'\{\{C:([A-Za-z0-9-]+)\}\}', content))
        for cid in sorted(linked_claims):
            if cid not in claim_index:
                errors.append(f'Manuscript claim anchor unknown {cid}')
            elif claim_index[cid]['verdict'] != 'supported':
                warnings.append(f'Manuscript claim {cid} is {claim_index[cid]["verdict"]}')
        if re.search(r'\[(?:TODO|CITATION NEEDED|SOURCE NEEDED)\]', content, re.I):
            warnings.append('Manuscript contains unresolved placeholder(s)')
        if len(content.strip()) > 200 and not cited:
            warnings.append('Manuscript has substantive content but no [@R0001] citations found; may use another citation format')
    else:
        warnings.append('No manuscript found; prose citation check skipped')

    if not records:
        warnings.append('No literature records: this is a blank template, not a completed review')
    if not evidences and claims:
        warnings.append('Claims exist but evidence ledger is empty')
    if not rows['search_log.csv']:
        warnings.append('Search log empty; no reproducible search is documented')

    report = {
        'status': 'ERRORS_FOUND' if errors else 'NO_STRUCTURAL_ERRORS',
        'scope': 'Structural consistency only; DOES NOT validate article content or scientific support',
        'counts': {'records': len(records), 'evidence_items': len(evidences),
                   'claims': len(claims), 'searches_logged': len(rows['search_log.csv']),
                   'citations_found': len(cited) if manuscript_exists else None},
        'errors': errors, 'warnings': list(dict.fromkeys(warnings))
    }
    outfile = p / 'audit_report.json'
    outfile.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote {outfile}\n' + json.dumps({'status': report['status'], 'errors': len(errors),
          'warnings': len(report['warnings'])}, indent=2))
    return 2 if errors else 0


def cli_prisma(args: argparse.Namespace) -> int:
    p = Path(args.project).expanduser().resolve()
    raw = read_rows(p / 'records.csv', SCHEMAS['records.csv'])
    canonical_path = p / 'deduped_records.csv'
    if not canonical_path.exists():
        raise ReviewError('PRISMA counts require dedupe to be run and manually checked first')
    canonical = read_rows(canonical_path, SCHEMAS['records.csv'])
    screened = read_rows(p / 'screening.csv', SCHEMAS['screening.csv'])
    sid = {r['record_id']: r['study_id'] for r in canonical}
    canonical_ids = set(sid)
    errors = []
    for s in screened:
        if s['record_id'] not in canonical_ids:
            errors.append(f'Screening {s["record_id"]} missing from canonical records; check duplicate map')
    if len({s['record_id'] for s in screened}) != len(screened):
        errors.append('Repeated record_id in screening.csv')
    decisions = {'include', 'exclude', 'pending'}
    full_options = {'include', 'exclude', 'pending', 'not_retrieved', 'not_applicable'}
    for s in screened:
        if s['title_abstract_decision'] not in decisions:
            errors.append(f'{s["record_id"]} missing/invalid title_abstract_decision')
        if s['full_text_decision'] not in full_options:
            errors.append(f'{s["record_id"]} missing/invalid full_text_decision')
        if s['full_text_decision'] == 'exclude' and not s['exclusion_reason']:
            errors.append(f'{s["record_id"]} missing full-text exclusion reason')
        if s['title_abstract_decision'] == 'exclude' and s['full_text_decision'] not in ('not_applicable',):
            errors.append(f'{s["record_id"]} title-excluded but full-text state not_applicable was expected')
        if s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'not_applicable':
            errors.append(f'{s["record_id"]} title-included but full text marked not_applicable')
    n_screened = len(screened)
    n_ta_excluded = sum(s['title_abstract_decision'] == 'exclude' for s in screened)
    n_sought = sum(s['title_abstract_decision'] == 'include' for s in screened)
    n_pending_ta = sum(s['title_abstract_decision'] == 'pending' for s in screened)
    n_not_retrieved = sum(s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'not_retrieved' for s in screened)
    n_pending_full = sum(s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'pending' for s in screened)
    n_full_excluded = sum(s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'exclude' for s in screened)
    included = [s for s in screened if s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'include']
    n_full_assessed = len(included) + n_full_excluded
    if len(screened) < len(canonical):
        errors.append(f'{len(canonical)-len(screened)} canonical records missing screening decision')
    missing_studies = [s['record_id'] for s in included if not sid.get(s['record_id'])]
    if missing_studies:
        errors.append('Cannot establish unique study count: missing study_id for included reports ' + ', '.join(missing_studies))
    unique_studies = len({sid[s['record_id']] for s in included if sid.get(s['record_id'])})
    by_reason = Counter(s['exclusion_reason'] for s in screened if s['title_abstract_decision'] == 'include' and s['full_text_decision'] == 'exclude')
    counts = {
        'identified_records': len(raw), 'duplicates_removed': len(raw)-len(canonical),
        'records_screened': n_screened, 'records_excluded_title_abstract': n_ta_excluded,
        'title_abstract_pending': n_pending_ta, 'reports_sought': n_sought,
        'reports_not_retrieved': n_not_retrieved, 'full_text_pending': n_pending_full,
        'reports_assessed_for_eligibility': n_full_assessed,
        'reports_excluded_full_text': n_full_excluded,
        'included_reports': len(included), 'included_unique_studies': unique_studies if not missing_studies else None,
        'full_text_exclusion_reasons': dict(by_reason)
    }
    if (n_pending_ta or n_pending_full):
        errors.append('Screening is incomplete; all pending decisions must be resolved before final flow')
    if n_full_assessed + n_not_retrieved + n_pending_full != n_sought:
        errors.append('PRISMA reconciliation failure: reports sought != assessed + not retrieved + pending')
    if n_full_excluded + len(included) != n_full_assessed:
        errors.append('PRISMA reconciliation failure in full text stage')
    status = 'INCOMPLETE: NOT FOR PUBLICATION' if errors else 'STRUCTURAL COUNTS RECONCILED: HUMAN CHECK REQUIRED'
    lines = ['# PRISMA-style flow count worksheet', '', f'**Status:** {status}', '',
             'These are computed counts from entered screening records. They do not certify PRISMA compliance.', '',
             '| Metric | Count |', '| --- | ---: |']
    for k, v in counts.items():
        if k != 'full_text_exclusion_reasons':
            lines.append(f'| {k.replace("_", " ").capitalize()} | {v if v is not None else "UNVERIFIED"} |')
    lines += ['', '## Full-text exclusion reasons', '']
    if by_reason:
        lines += [f'- {k}: {v}' for k,v in sorted(by_reason.items())]
    else:
        lines += ['- None recorded']
    lines += ['', '## Data validation', '']
    lines += [f'- {e}' for e in errors] if errors else ['- No structural count errors; author must verify protocol, eligibility, and independent screening.']
    (p / 'prisma_counts.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (p / 'prisma_counts.json').write_text(json.dumps({'status': status, 'counts': counts, 'errors': errors}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': status, 'counts': counts, 'errors': errors}, indent=2))
    return 2 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    init = sub.add_parser('init', help='Create a blank review workspace; never overwrites existing files')
    init.add_argument('--out', required=True)
    init.add_argument('--topic', required=True)
    init.add_argument('--type', choices=['narrative-critical','systematic','scoping'], default='narrative-critical')
    init.set_defaults(func=cli_init)
    dedupe = sub.add_parser('dedupe', help='Suggest duplicate bibliographic records; review merges manually')
    dedupe.add_argument('--input', required=True)
    dedupe.add_argument('--out', required=True)
    dedupe.set_defaults(func=cli_dedupe)
    audit = sub.add_parser('audit', help='Validate references, claims, evidence, statuses, and manuscript citation keys')
    audit.add_argument('--project', required=True)
    audit.add_argument('--manuscript')
    audit.set_defaults(func=cli_audit)
    prisma = sub.add_parser('prisma', help='Compute worksheet counts for reports and studies from completed screening')
    prisma.add_argument('--project', required=True)
    prisma.set_defaults(func=cli_prisma)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ReviewError, OSError, UnicodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
