from base import TestBase

class NewAssignTest(TestBase):
    snippet_dir = "newCase/assign"
    def test_assign_class(self):
        self.validate_snippet(self.get_snippet_path("assign_class"))


    def test_assign_function(self):
        self.validate_snippet(self.get_snippet_path("assign_function"))


    def test_assign_swap(self):
        self.validate_snippet(self.get_snippet_path("assign_swap"))


    def test_assign_variable(self):
        self.validate_snippet(self.get_snippet_path("assign_variable"))