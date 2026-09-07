"""Real-ciphertext regression checks; optional original-page normalization fixture."""
import contextlib
import hashlib
import io
import json
import os
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch
import oracle

class OracleRegressionTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('ARWEAVE3_SOURCE'), 'set ARWEAVE3_SOURCE to the original HTML')
    def test_original_proceed_accepts_empty_cells_without_padding(self):
        witness = hashlib.sha256(b'arweave3 short public regression fixture').hexdigest()[:28]
        letters = iter(witness.upper())
        cells = ['' if i in (0, 7, 17, 31) else next(letters) for i in range(32)]
        payload = dict(ciphertext=oracle.PZL8_CIPHERTEXT_B64, answer=oracle.PZL8_ANSWER,
                       target=oracle.PZL8_ADDRESS, witness=witness, cells=cells)
        helper = pathlib.Path(__file__).with_name('original_page_fixture.js')
        result = subprocess.run(['node', str(helper), os.environ['ARWEAVE3_SOURCE']],
                                input=json.dumps(payload), text=True, capture_output=True,
                                check=True, timeout=30)
        fixture = json.loads(result.stdout)
        self.assertTrue(fixture['form_roundtrip_ok'])
        args = dict(ciphertext_b64=fixture['ciphertext'], target=oracle.PZL8_ADDRESS)
        self.assertEqual(oracle.check(''.join(cells), **args), (True, oracle.PZL8_ADDRESS))
        self.assertFalse(oracle.check(''.join(c or ' ' for c in cells), **args)[0])

    def test_sibling_is_not_this_escrow(self):
        args = dict(ciphertext_b64=oracle.PZL8_CIPHERTEXT_B64, lowercase=False)
        self.assertEqual(oracle.check(oracle.PZL8_ANSWER, target=oracle.PZL8_ADDRESS, **args),
                         (True, oracle.PZL8_ADDRESS))
        self.assertEqual(oracle.check(oracle.PZL8_ANSWER, **args),
                         (False, oracle.PZL8_ADDRESS))

    @unittest.skipUnless(os.environ.get('ARWEAVE3_SOURCE'), 'set ARWEAVE3_SOURCE to the original HTML')
    def test_original_page_fixture_normalization_and_output(self):
        # Fixed calibration text, not a proposed answer to the puzzle.
        witness = hashlib.sha256(b'arweave3 public regression fixture').hexdigest()[:32]
        helper = pathlib.Path(__file__).with_name('original_page_fixture.js')
        payload = {'ciphertext': oracle.PZL8_CIPHERTEXT_B64, 'answer': oracle.PZL8_ANSWER,
                   'target': oracle.PZL8_ADDRESS, 'witness': witness}
        result = subprocess.run(['node', str(helper), os.environ['ARWEAVE3_SOURCE']],
                                input=json.dumps(payload), text=True, capture_output=True,
                                check=True, timeout=30)
        fixture = json.loads(result.stdout)
        self.assertTrue(fixture['roundtrip_ok'])
        args = dict(ciphertext_b64=fixture['ciphertext'], target=oracle.PZL8_ADDRESS)
        self.assertEqual(oracle.check(witness.upper(), **args), (True, oracle.PZL8_ADDRESS))
        self.assertEqual(oracle.check(witness, ciphertext_b64=fixture['ciphertext']),
                         (False, oracle.PZL8_ADDRESS))
        self.assertFalse(oracle.check(' ' + witness, **args)[0])
        output = io.StringIO()
        with patch.object(oracle, 'CIPHERTEXT_B64', fixture['ciphertext']), \
             patch.object(oracle, 'ESCROW', oracle.PZL8_ADDRESS), \
             patch.object(sys, 'argv', ['oracle.py', '--stdin']), \
             patch.object(sys, 'stdin', io.StringIO(witness.upper() + '\n')), \
             contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                oracle.main()
        self.assertEqual(stopped.exception.code, 0)
        self.assertEqual(output.getvalue(), 'MATCH ' + oracle.PZL8_ADDRESS + '\n')

if __name__ == '__main__':
    unittest.main()
