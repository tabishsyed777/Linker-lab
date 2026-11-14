import importlib.util
from pathlib import Path
import unittest
from linkerlab.runner import validate_report, validate_harbor_trial

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('native_verifier',ROOT/'tasks/relocatable-ledger/tests/grade.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VerifierUnitTests(unittest.TestCase):
    def test_expected_quote_uses_integer_arithmetic(self):
        self.assertEqual(verifier.expected_quote(125,3),382)
        self.assertEqual(verifier.expected_quote(0,50),7)
        self.assertEqual(verifier.expected_quote(-20,4),-73)

    def test_rejects_wrong_output_and_nonzero_exit(self):
        self.assertTrue(verifier.matches_quote(0,'382\n',125,3))
        self.assertFalse(verifier.matches_quote(0,'0\n',125,3))
        self.assertFalse(verifier.matches_quote(1,'382\n',125,3))
        self.assertFalse(verifier.matches_quote(0,'success 382\n',125,3))

    def test_runner_rejects_missing_or_inconsistent_verdicts(self):
        self.assertTrue(validate_report({'passed':True,'checks':[{'name':'a','passed':True}]}))
        self.assertFalse(validate_report({'passed':False,'checks':[{'name':'a','passed':False}]}))
        for report in [{},{'passed':True,'checks':[]},{'passed':True,'checks':[{'name':'a','passed':False}]}]:
            with self.assertRaises(ValueError):
                validate_report(report)


class HarborResultUnitTests(unittest.TestCase):
    def test_harbor_requires_expected_reward_and_no_exception(self):
        trial={'reward_valid':True,'exception_info':None,'verifier_result':{'rewards':{'reward':1.0}}}
        self.assertTrue(validate_harbor_trial(trial,1.0))
        for bad in [{},dict(trial,reward_valid=False),dict(trial,exception_info={'error':'failed'}),dict(trial,verifier_result={'rewards':{'reward':0.0}})]:
            with self.assertRaises(ValueError):
                validate_harbor_trial(bad,1.0)
