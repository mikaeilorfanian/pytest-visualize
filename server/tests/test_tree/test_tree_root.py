from pathlib import Path

from pytest import fixture

from tree import TreeRoot


@fixture
def tree_root():
    return TreeRoot()


class TestTreeRootJSONHasCorrectPathAttribute:
    def test_with_one_module_at_root_level(self, tree_root):
        tree_root.get_or_create_module('test_sth.py')

        assert len(tree_root.json_paths_only) == 1
        assert tree_root.json_paths_only[0]['path'] == 'test_sth.py'

    def test_with_two_different_modules_at_root_level(self, tree_root):
        tree_root.get_or_create_module('test_sth.py')
        tree_root.get_or_create_module('test_sth1.py')

        assert len(tree_root.json_paths_only) == 2
        assert tree_root.json_paths_only[0]['path'] == 'test_sth.py'
        assert tree_root.json_paths_only[1]['path'] == 'test_sth1.py'

    def test_with_one_module_within_package_and_one_at_root_level(self, tree_root):
        tree_root.get_or_create_module('tests/test_sth.py')

        assert len(tree_root.json_paths_only) == 1
        package = tree_root.json_paths_only[0]
        assert package['path'] == 'tests'

        module_within_package = package['children'][0]
        assert Path(module_within_package['path']) == Path('tests/test_sth.py')

        tree_root.get_or_create_module('test_sth.py')
        root_module = tree_root.json_paths_only[1]
        assert root_module['path'] == 'test_sth.py'

    def test_one_module_within_two_levels_deep_test_packages(self, tree_root):
        tree_root.get_or_create_module('tests/test_sub/test_sth.py')

        assert len(tree_root.json_paths_only) == 1
        package = tree_root.json_paths_only[0]
        assert package['path'] == 'tests'

        sub_package = package['children'][0]
        assert sub_package['name'] == 'test_sub'
        assert Path(sub_package['path']) == Path('tests/test_sub')

        test_module = sub_package['children'][0]
        assert Path(test_module['path']) == Path('tests/test_sub/test_sth.py')

    def test_one_module_within_three_levels_deep_test_packages(self, tree_root):
        tree_root.get_or_create_module('tests/test_sub1/test_sub2/test_sth.py')

        assert len(tree_root.json_paths_only) == 1
        package = tree_root.json_paths_only[0]
        assert package['path'] == 'tests'

        sub_package1 = package['children'][0]
        assert sub_package1['name'] == 'test_sub1'
        assert Path(sub_package1['path']) == Path('tests/test_sub1')

        sub_package2 = sub_package1['children'][0]
        assert Path(sub_package2['path']) == Path('tests/test_sub1/test_sub2')

        test_module = sub_package2['children'][0]
        assert Path(test_module['path']) == Path('tests/test_sub1/test_sub2/test_sth.py')

    def test_two_modules_within_the_same_nested_package(self, tree_root):
        tree_root.get_or_create_module('tests/test_sub/test_sth1.py')
        tree_root.get_or_create_module('tests/test_sub/test_sth2.py')

        package = tree_root.json_paths_only[0]
        sub_package = package['children'][0]
        assert Path(sub_package['path']) == Path('tests/test_sub')

        test_module1 = sub_package['children'][0]
        assert Path(test_module1['path']) == Path('tests/test_sub/test_sth1.py')

        test_module2 = sub_package['children'][1]
        assert Path(test_module2['path']) == Path('tests/test_sub/test_sth2.py')

    def test_two_modules_in_different_levels_of_nesting(self, tree_root):
        tree_root.get_or_create_module('tests/test_sub1/test_sth1.py')
        tree_root.get_or_create_module('tests/test_sub2/test_sub3/test_sth2.py')

        package = tree_root.json_paths_only[0]
        sub_package = package['children'][0]
        assert Path(sub_package['path']) == Path('tests/test_sub1')

        test_module = sub_package['children'][0]
        assert Path(test_module['path']) == Path('tests/test_sub1/test_sth1.py')

        package = tree_root.json_paths_only[0]
        sub_package = package['children'][1]
        assert Path(sub_package['path']) == Path('tests/test_sub2')

        sub_sub_package = sub_package['children'][0]
        assert Path(sub_sub_package['path']) == Path('tests/test_sub2/test_sub3')

        test_module = sub_sub_package['children'][0]
        assert Path(test_module['path']) == Path('tests/test_sub2/test_sub3/test_sth2.py')


class TestTreeRootJson:
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
