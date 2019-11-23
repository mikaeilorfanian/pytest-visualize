import tree


class TestTreeRootLevel:
    def test_adding_one_test_module(self):
        test_obj = tree.ObjTest('test_sth.py', 'test_one', True, 'test_sth.py::test_one')
        test_tree = tree.Tree()
        test_tree.add(test_obj)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict) == 1
        assert test_tree_dict[0]['name'] == 'test_sth.py'
        assert test_tree_dict[0]['file'] is True
        assert 'children' in test_tree_dict[0]

    def test_one_module_with_one_collected_test_function(self):
        test_obj = tree.ObjTest('test_sth.py', 'test_one', None, 'test_sth.py::test_one')
        test_tree = tree.Tree()
        test_tree.add(test_obj)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict) == 1
        assert test_tree_dict[0]['name'] == 'test_sth.py'
        assert test_tree_dict[0]['file'] is True
        assert len(test_tree_dict[0]['children']) == 1

        test_case = test_tree_dict[0]['children'][0]
        assert test_case['name'] == 'test_one'
        assert test_case['id'] == 'test_sth.py::test_one'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

    def test_one_module_with_two_collected_test_functions(self):
        test_obj1 = tree.ObjTest('test_sth.py', 'test_one', None, 'test_sth.py::test_one')
        test_obj2 = tree.ObjTest('test_sth.py', 'test_two', None, 'test_sth.py::test_two')
        test_tree = tree.Tree()
        test_tree.add(test_obj1)
        test_tree.add(test_obj2)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict) == 1
        assert test_tree_dict[0]['name'] == 'test_sth.py'
        assert test_tree_dict[0]['file'] is True
        assert len(test_tree_dict[0]['children']) == 2

        test_case = test_tree_dict[0]['children'][0]
        assert test_case['name'] == 'test_one'
        assert test_case['id'] == 'test_sth.py::test_one'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

        test_case = test_tree_dict[0]['children'][1]
        assert test_case['name'] == 'test_two'
        assert test_case['id'] == 'test_sth.py::test_two'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

    def test_one_module_with_one_test_class_with_one_test_method(self):
        test_obj1 = tree.ObjTest('test_sth.py', 'test_one', None, 'test_sth.py::TestKlass::test_one')
        test_tree = tree.Tree()
        test_tree.add(test_obj1)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict[0]['children']) == 1
        test_class = test_tree_dict[0]['children'][0]
        assert test_class['name'] == 'TestKlass'
        assert test_class['testKlass'] is True
        assert len(test_class['children']) == 1

        test_case = test_class['children'][0]
        assert test_case['name'] == 'test_one'
        assert test_case['id'] == 'test_sth.py::TestKlass::test_one'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

    def test_one_module_with_one_test_class_with_multiple_test_methods(self):
        test_obj1 = tree.ObjTest('test_sth.py', 'test_one', None, 'test_sth.py::TestKlass::test_one')
        test_obj2 = tree.ObjTest('test_sth.py', 'test_two', None, 'test_sth.py::TestKlass::test_two')
        test_tree = tree.Tree()
        test_tree.add(test_obj1)
        test_tree.add(test_obj2)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict[0]['children']) == 1
        test_class = test_tree_dict[0]['children'][0]
        assert test_class['name'] == 'TestKlass'
        assert test_class['testKlass'] is True
        assert len(test_class['children']) == 2

        test_case = test_class['children'][0]
        assert test_case['name'] == 'test_one'
        assert test_case['id'] == 'test_sth.py::TestKlass::test_one'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

        test_case = test_class['children'][1]
        assert test_case['name'] == 'test_two'
        assert test_case['id'] == 'test_sth.py::TestKlass::test_two'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

    def test_one_module_with_multiple_test_classes(self):
        test_obj1 = tree.ObjTest('test_sth.py', 'test_one', None, 'test_sth.py::TestKlass1::test_one')
        test_obj2 = tree.ObjTest('test_sth.py', 'test_two', None, 'test_sth.py::TestKlass2::test_two')
        test_tree = tree.Tree()
        test_tree.add(test_obj1)
        test_tree.add(test_obj2)
        test_tree_dict = test_tree.json

        assert len(test_tree_dict[0]['children']) == 2

        test_class = test_tree_dict[0]['children'][0]
        assert test_class['name'] == 'TestKlass1'
        assert len(test_class['children']) == 1
        test_case = test_class['children'][0]
        assert test_case['name'] == 'test_one'
        assert test_case['id'] == 'test_sth.py::TestKlass1::test_one'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']

        test_class = test_tree_dict[0]['children'][1]
        assert test_class['name'] == 'TestKlass2'
        assert len(test_class['children']) == 1
        test_case = test_class['children'][0]
        assert test_case['name'] == 'test_two'
        assert test_case['id'] == 'test_sth.py::TestKlass2::test_two'
        assert test_case['singleTest'] == True
        assert test_case['file'] is False
        assert test_case['testRan'] is False
        assert test_case['passed'] is None
        assert not test_case['errorRepr']
