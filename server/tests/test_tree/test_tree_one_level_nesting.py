import tree


class TestTreeWithOneLevelOfNesting:
    def test_adding_one_test_module_within_package(self):
        test_obj = tree.ObjTest('tests/test_sth1.py', 'test_one', True, 'tests/test_sth1.py::test_one')
        test_tree = tree.Tree()
        test_tree.add(test_obj)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict) == 1
        assert test_tree_dict[0]['name'] == 'test_sth.py'
        assert test_tree_dict[0]['file'] is True
        assert 'children' in test_tree_dict[0]
