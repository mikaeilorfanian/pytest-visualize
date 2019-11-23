from pathlib import Path
import tree


class TestObjTestKlass:
    def test_post_init_method(self):
        test_obj = tree.ObjTest('test_sth.py', 'test_one', True, 'test_sth.py::test_one')
        assert isinstance(test_obj.path_obj, Path)

        test_obj = tree.ObjTest('tests/test_sth1.py', 'test_one', True, 'tests/test_sth1.py::test_one')
        assert isinstance(test_obj.path_obj, Path)

    def test_module_is_at_the_root_of_the_directory_tree(self):
        test_obj = tree.ObjTest('test_sth.py', 'test_one', True, 'test_sth.py::test_one')
        assert test_obj.is_at_root is True

        test_obj = tree.ObjTest('tests/test_sth1.py', 'test_one', True, 'tests/test_sth1.py::test_one')
        assert test_obj.is_at_root is False

    def test_obj_is_test_class(self):
        test_obj = tree.ObjTest('test_sth.py', 'test_one', True, 'test_sth.py::test_one')
        assert test_obj.has_test_class is False

        test_obj = tree.ObjTest('tests/test_sth1.py', 'test_one', True, 'tests/test_sth1.py::test_one')
        assert test_obj.has_test_class is False

        test_obj = tree.ObjTest('test_sth.py', 'test_one', True, 'test_sth.py::TestKlass::test_one')
        assert test_obj.has_test_class is True

    def test_obj_is_within_package(self):
        test_obj = tree.ObjTest('tests/test_sth1.py', 'test_one', True, 'tests/test_sth1.py::test_one')
        assert test_obj.is_within_package is True
