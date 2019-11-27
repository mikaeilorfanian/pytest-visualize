from tree import TreeRoot


class TestTreeRoot:
    def test_create_root_package(self):
        tree = TreeRoot()
        assert tree.json == list()

    def test_add_module_at_root_level(self):
        tree = TreeRoot()
        tree.get_or_create_module('test_sth.py')

        assert len(tree.json) == 1
        assert tree.json[0]['name'] == 'test_sth.py'
        assert tree.json[0]['isModule'] is True

    def test_add_same_module_twice(self):
        tree = TreeRoot()
        tree.get_or_create_module('test_sth.py')
        tree.get_or_create_module('test_sth.py')

        assert len(tree.json) == 1
        assert tree.json[0]['name'] == 'test_sth.py'
        assert tree.json[0]['isModule'] is True

    def test_add_two_modules_at_root_level(self):
        tree = TreeRoot()
        tree.get_or_create_module('test_sth.py')
        tree.get_or_create_module('test_sth1.py')

        assert len(tree.json) == 2
        assert tree.json[0]['name'] == 'test_sth.py'
        assert tree.json[0]['isModule'] is True
        assert tree.json[1]['name'] == 'test_sth1.py'
        assert tree.json[1]['isModule'] is True

    def test_add_module_within_package_and_at_root_level(self):
        tree = TreeRoot()
        tree.get_or_create_module('tests/test_sth.py')

        assert len(tree.json) == 1
        package = tree.json[0]
        assert package['name'] == 'tests'
        assert package['isPackage'] is True
        assert len(package['children']) == 1

        module_within_package = package['children'][0]
        assert module_within_package['name'] == 'test_sth.py'
        assert module_within_package['isModule'] is True
        assert len(module_within_package['children']) == 0

        tree.get_or_create_module('test_sth.py')
        assert len(tree.json) == 2
        root_module = tree.json[1]
        assert root_module['isModule'] is True
        assert root_module['name'] == 'test_sth.py'

    def test_add_module_within_two_nested_packages(self):
        tree = TreeRoot()
        tree.get_or_create_module('tests/tests1/test_sth.py')

        assert len(tree.json) == 1
        package = tree.json[0]
        assert package['name'] == 'tests'
        assert package['isPackage'] is True
        assert len(package['children']) == 1

        sub_package = package['children'][0]
        assert sub_package['name'] == 'tests1'
        assert sub_package['isPackage'] is True
        assert len(sub_package['children']) == 1

        module = sub_package['children'][0]
        assert module['name'] == 'test_sth.py'
        assert module['isModule'] is True
        assert len(module['children']) == 0
