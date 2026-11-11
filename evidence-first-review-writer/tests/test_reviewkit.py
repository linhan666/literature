"""Synthetic fixtures only: no claims about real scientific papers are made here."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import reviewkit
import verify_dois
import search_epmc
from unittest.mock import patch


def row(**kwargs):
    return kwargs


class ReviewKitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'review'
        reviewkit.cli_init(argparse.Namespace(out=str(self.project), topic='Synthetic model review',
                                             type='narrative-critical'))

    def put(self, fname, rows):
        reviewkit.write_rows(self.project / fname, reviewkit.SCHEMAS[fname], rows)

    def assert_report(self, field, expected):
        obj = json.loads((self.project / 'audit_report.json').read_text(encoding='utf-8'))
        self.assertEqual(obj[field], expected)

    def prepare(self):
        # Fake bibliography deliberately uses test-only fabricated DOI and title.
        self.put('records.csv', [
            row(record_id='R0001', study_id='S0001', title='Synthetic Paper Alpha',
                year='2025', doi='10.9999/synthetic.a', metadata_status='verified',
                access_level='full_text', peer_review_status='peer_reviewed'),
            row(record_id='R0002', study_id='S0001', title='Synthetic Paper Alpha',
                year='2025', doi='https://doi.org/10.9999/synthetic.a',
                metadata_status='unverified', access_level='abstract'),
            row(record_id='R0003', study_id='S0002', title='Synthetic Paper Beta',
                year='2024', doi='10.9999/synthetic.b', metadata_status='verified',
                access_level='full_text'),
            row(record_id='R0004', study_id='S0003', title='Synthetic Paper Alpha',
                year='2025', doi='10.9999/synthetic.c', metadata_status='verified',
                access_level='full_text'),
        ])
        self.put('search_log.csv', [row(search_id='Q0001', database='Synthetic index',
                                        query='synthetic', run_date='2026-01-01', retrieved_count='4')])

    def test_init_does_not_overwrite_user_edits(self):
        brief = self.project / 'review_brief.md'
        brief.write_text('My edits', encoding='utf-8')
        reviewkit.cli_init(argparse.Namespace(out=str(self.project), topic='Other', type='scoping'))
        self.assertEqual(brief.read_text(encoding='utf-8'), 'My edits')
        self.assertIn('record_id', (self.project / 'records.csv').read_text(encoding='utf-8'))

    def test_dedupe_and_doi_conflict(self):
        self.prepare()
        reviewkit.cli_dedupe(argparse.Namespace(input=str(self.project / 'records.csv'), out=str(self.project)))
        kept = reviewkit.read_rows(self.project / 'deduped_records.csv')
        self.assertEqual(len(kept), 3)
        dups = reviewkit.read_rows(self.project / 'duplicate_map.csv')
        self.assertEqual(len(dups), 1)
        self.assertEqual(dups[0]['canonical_id'], 'R0001')
        conflicts = reviewkit.read_rows(self.project / 'dedupe_conflicts.csv')
        self.assertTrue(conflicts, 'Different DOIs with same title/year must be flagged')

    def test_audit_valid_structural_links(self):
        self.prepare()
        self.put('evidence.csv', [row(evidence_id='E0001', record_id='R0001', study_id='S0001',
                                      claim_id='CLM001', section_or_page='Results, Table 1',
                                      evidence_type='primary_fulltext', support_status='supports')])
        self.put('claims.csv', [row(claim_id='CLM001', claim_text='Synthetic example claim',
                                    verdict='supported', evidence_ids='E0001', strength='descriptive')])
        (self.project / 'manuscript.md').write_text('A test-supported statement {{C:CLM001}} [@R0001].', encoding='utf-8')
        status = reviewkit.cli_audit(argparse.Namespace(project=str(self.project), manuscript=None))
        self.assertEqual(status, 0)
        self.assert_report('status', 'NO_STRUCTURAL_ERRORS')

    def test_audit_rejects_false_links_and_inaccessible_fulltext(self):
        self.prepare()
        self.put('evidence.csv', [row(evidence_id='E0007', record_id='R0002', claim_id='CLM009',
                                      evidence_type='primary_fulltext', support_status='supports')])
        self.put('claims.csv', [row(claim_id='CLM009', claim_text='Unsupported synthetic claim',
                                    verdict='supported', evidence_ids='E0999')])
        (self.project / 'manuscript.md').write_text('Incorrect source [@R9999].', encoding='utf-8')
        status = reviewkit.cli_audit(argparse.Namespace(project=str(self.project), manuscript=None))
        self.assertEqual(status, 2)
        errors = json.loads((self.project / 'audit_report.json').read_text())['errors']
        self.assertTrue(any('R9999' in e for e in errors))
        self.assertTrue(any('E0999' in e for e in errors))
        self.assertTrue(any('non-full-text' in e for e in errors))

    def test_prisma_complete_and_incomplete(self):
        self.prepare()
        reviewkit.cli_dedupe(argparse.Namespace(input=str(self.project / 'records.csv'), out=str(self.project)))
        self.put('screening.csv', [
            row(record_id='R0001', title_abstract_decision='include', full_text_decision='include'),
            row(record_id='R0003', title_abstract_decision='exclude', full_text_decision='not_applicable'),
            row(record_id='R0004', title_abstract_decision='include', full_text_decision='exclude',
                exclusion_reason='Wrong method'),
        ])
        code = reviewkit.cli_prisma(argparse.Namespace(project=str(self.project)))
        self.assertEqual(code, 0)
        report = json.loads((self.project / 'prisma_counts.json').read_text())
        self.assertEqual(report['counts']['identified_records'], 4)
        self.assertEqual(report['counts']['duplicates_removed'], 1)
        self.assertEqual(report['counts']['included_unique_studies'], 1)
        self.assertEqual(report['counts']['reports_assessed_for_eligibility'], 2)
        self.assertEqual(report['counts']['reports_excluded_full_text'], 1)
        self.put('screening.csv', [row(record_id='R0001', title_abstract_decision='include',
                                        full_text_decision='pending')])
        self.assertEqual(reviewkit.cli_prisma(argparse.Namespace(project=str(self.project))), 2)

    def test_europe_pmc_adapter_appends_an_honest_log(self):
        synthetic_payload = {
            'hitCount': 1,
            'resultList': {'result': [{
                'id': 'TEST0001', 'source': 'PPR', 'doi': '10.9999/placeholder',
                'title': 'Synthetic Preprint', 'authorString': 'Example Author',
                'pubYear': '2026', 'abstractText': 'A mock abstract'
            }]},
            'nextCursorMark': ''
        }
        args = argparse.Namespace(project=str(self.project), query='mock drug discovery query',
                                  max_results=10, page_size=10, timeout=1, delay=0)
        with patch.object(search_epmc, 'fetch_page', return_value=synthetic_payload) as fetch:
            result = search_epmc.run(args)
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(result['retrieved'], 1)
        sources = reviewkit.read_rows(self.project / 'records.csv')
        self.assertEqual(sources[0]['metadata_status'], 'unverified')
        self.assertEqual(sources[0]['peer_review_status'], 'preprint')
        self.assertEqual(sources[0]['access_level'], 'abstract')
        logs = reviewkit.read_rows(self.project / 'search_log.csv')
        self.assertEqual(logs[0]['query'], 'mock drug discovery query')
        self.assertEqual(logs[0]['retrieved_count'], '1')

    def test_europe_pmc_adapter_does_not_write_on_network_failure(self):
        args = argparse.Namespace(project=str(self.project), query='mock failing query',
                                  max_results=10, page_size=10, timeout=1, delay=0)
        with patch.object(search_epmc, 'fetch_page', side_effect=TimeoutError('mock timeout')):
            with self.assertRaises(TimeoutError):
                search_epmc.run(args)
        self.assertFalse(reviewkit.read_rows(self.project / 'records.csv'))
        self.assertFalse(reviewkit.read_rows(self.project / 'search_log.csv'))

    def test_crossref_comparison_is_candidate_not_claim_proof(self):
        sample = {'record_id': 'R0001', 'doi': '10.9999/synthetic.a',
                  'title': 'Synthetic Paper Alpha', 'year': '2025'}
        record = {'DOI': '10.9999/synthetic.a', 'title': ['Synthetic Paper Alpha'],
                  'published': {'date-parts': [[2025, 2, 1]]}}
        verdict = verify_dois.compare(sample, record)
        self.assertEqual(verdict['identity_check'], 'likely_match')
        self.assertIn('does not validate any claim', verdict['note'])


if __name__ == '__main__':
    unittest.main()
