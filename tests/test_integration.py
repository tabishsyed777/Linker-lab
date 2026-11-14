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
            details=(out/'report.json').read_text() if (out/'report.json').exists() else ''
            self.assertEqual(result.returncode,0,result.stdout+result.stderr+details)
            report=json.loads((out/'report.json').read_text())
            self.assertTrue(report['oracle']['passed'])
            self.assertFalse(report['nop']['passed'])
            self.assertFalse(report['static_shortcut']['passed'])
            self.assertGreaterEqual(len(report['oracle']['checks']),10)
            self.assertTrue((out/'report.html').is_file())
            repeated=subprocess.run([sys.executable,'-m','linkerlab','demo','--output',str(out)],capture_output=True,text=True,timeout=10)
            self.assertNotEqual(repeated.returncode,0)

    def test_reference_with_standard_build_directory_permissions(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            temporary=Path(temp)
            candidate=temporary/'CMakeLists.txt'
            reference=(root/'tasks/relocatable-ledger/solution/CMakeLists.txt').read_text()
            candidate.write_text(reference+'\nfile(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/restricted")\nfile(WRITE "${CMAKE_BINARY_DIR}/restricted/marker" "build output")\nfile(CHMOD "${CMAKE_BINARY_DIR}/restricted" PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)\n')
            out=temporary/'grade'
            result=subprocess.run([sys.executable,'-m','linkerlab','grade','--candidate',str(candidate),'--output',str(out)],capture_output=True,text=True,timeout=180)
            details=(out/'report.json').read_text() if (out/'report.json').exists() else ''
            self.assertEqual(result.returncode,0,result.stdout+result.stderr+details)
