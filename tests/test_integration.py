import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class NativeIntegrationTests(unittest.TestCase):
    def test_reference_passes_nop_and_static_shortcut_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'demo'
            result=subprocess.run([sys.executable,'-m','linkerlab','demo','--output',str(out)],capture_output=True,text=True,timeout=240)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            report=json.loads((out/'report.json').read_text())
            self.assertTrue(report['oracle']['passed'])
            self.assertFalse(report['nop']['passed'])
            self.assertFalse(report['static_shortcut']['passed'])
            self.assertGreaterEqual(len(report['oracle']['checks']),10)
            self.assertTrue((out/'report.html').is_file())
            repeated=subprocess.run([sys.executable,'-m','linkerlab','demo','--output',str(out)],capture_output=True,text=True,timeout=10)
            self.assertNotEqual(repeated.returncode,0)
