
import os

from base import TestBase

class NewCallTest(TestBase):
    snippet_dir = "newCase/calls"

    def test_class_call(self):
        self.validate_snippet(self.get_snippet_path("class_call"))

    def test_ext_insider_call(self):
        self.validate_snippet(self.get_snippet_path("ext_insider_call"))

    def test_external_call(self):
        self.validate_snippet(self.get_snippet_path("external_call"))

    def test_insider_call(self):
        self.validate_snippet(self.get_snippet_path("insider_call"))

    def test_insider_ext_call(self):
        self.validate_snippet(self.get_snippet_path("insider_ext_call"))
