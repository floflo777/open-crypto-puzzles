#!/usr/bin/env python3
"""Regression checks for exact escrow matching and secret-free CLI output."""
import contextlib
import io
import sys
import unittest
from unittest.mock import patch
import oracle

class OracleRegressionTests(unittest.TestCase):
    def test_real_sibling_matches_only_its_own_address(self):
        with patch.object(oracle,'CIPHERTEXT_B64',oracle.PZL8_CIPHERTEXT_B64):
            self.assertEqual(oracle.check(oracle.PZL8_ANSWER,target=oracle.PZL8_ADDRESS),(True,oracle.PZL8_ADDRESS))
            self.assertEqual(oracle.check(oracle.PZL8_ANSWER),(False,oracle.PZL8_ADDRESS))

    def test_stdin_prints_address_without_answer(self):
        output=io.StringIO()
        with patch.object(oracle,'CIPHERTEXT_B64',oracle.PZL8_CIPHERTEXT_B64), patch.object(oracle,'ESCROW',oracle.PZL8_ADDRESS), patch.object(sys,'argv',['oracle.py','--stdin']), patch.object(sys,'stdin',io.StringIO(oracle.PZL8_ANSWER+'\n')), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as result:oracle.main()
        self.assertEqual(result.exception.code,0)
        self.assertEqual(output.getvalue(),'MATCH '+oracle.PZL8_ADDRESS+'\n')
        self.assertNotIn(oracle.PZL8_ANSWER,output.getvalue())

if __name__=='__main__':unittest.main()
