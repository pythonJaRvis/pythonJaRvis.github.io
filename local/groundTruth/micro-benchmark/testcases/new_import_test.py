

import os

from base import TestBase

class newArgsTest(TestBase):
    snippet_dir = "newCase/args"

    def test_assign_return(self):
        self.validate_snippet(self.get_snippet_path("assign_return"))

    def test_class_args(self):
        self.validate_snippet(self.get_snippet_path("class_args"))

    def test_class_default_args(self):
        self.validate_snippet(self.get_snippet_path("class_default_args"))

    def test_default_args(self):
        self.validate_snippet(self.get_snippet_path("default_args"))
