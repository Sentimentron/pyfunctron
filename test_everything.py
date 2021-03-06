import unittest
import base64
from pyfunctron import *

class TestInvoke(unittest.TestCase):

    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.url = "http://localhost:8081/"

    def get_path(self, test_fn):
        return os.path.join(self.path, test_fn, "Dockerfile")

    @classmethod
    def format_out(cls, out):
        if out is None:
            return out
        return base64.b64decode(out)

    def test_connection(self):
        with FunctronInvocation("test-hello-world") as fi:
            self.assertTrue(fi.test_connection(self.url))

    def test_basic_stdout(self):
        with FunctronInvocation("test-hello-world") as fi:
            fi.set_dockerfile(self.get_path("test_fn_hello_world"))
            fi.add_files(os.path.join(self.path, "test_fn_hello_world"))
            response = fi.invoke(self.url)
            self.assertEqual(None, response.build_out.stderr, self.format_out(response.build_out.stderr))
            self.assertEqual(None, response.cmd_out.stderr, self.format_out(response.cmd_out.stderr))
            self.assertEqual(b"Hello World!\n", response.cmd_out.stdout)

    def test_build_failure(self):
        with FunctronInvocation("test-hello-world-build-failure") as fi:
            fi.set_dockerfile(self.get_path("test_fn_build_failure"))
            fi.add_files(os.path.join(self.path, "test_fn_build_failure"))
            response = fi.invoke(self.url, None, 1.0)
            self.assertNotEqual(None, response.build_out.stderr)
            self.assertEqual(None, response.cmd_out.stderr)

    def test_invoke_failure(self):
        with FunctronInvocation("test-hello-world-invoke-failure") as fi:
            fi.set_dockerfile(self.get_path("test_fn_invoke_failure"))
            fi.add_files(os.path.join(self.path, "test_fn_invoke_failure"))
            response = fi.invoke(self.url, None, 1.0)
            self.assertEqual(None, response.build_out.stderr)
            self.assertNotEqual(None, response.cmd_out.stderr)

    def test_with_stdin(self):
        with FunctronInvocation("test-hello-world-stdin") as fi:
            fi.set_dockerfile(self.get_path("test_fn_hello_world"))
            fi.add_files(os.path.join(self.path, "test_fn_stdin"))
            response = fi.invoke(self.url, "Functron User!".encode("utf8"), 1.0)
            self.assertEqual(None, response.build_out.stderr)
            self.assertEqual(None, response.cmd_out.stderr)
            self.assertEqual(b"Hello Functron User!\n", response.cmd_out.stdout)

    def test_timeout(self):
        with FunctronInvocation("test-hello-world-timeout") as fi:
            fi.set_dockerfile(self.get_path("test_fn_hello_world"))
            fi.add_files(os.path.join(self.path, "test_fn_exceed_timeout"))
            response = fi.invoke(self.url, None, 1.0)
            self.assertEqual(None, response.build_out.stderr)
            self.assertEqual(None, response.cmd_out.stderr)
            self.assertNotEqual(b"Hello World!\n", response.cmd_out.stdout)


