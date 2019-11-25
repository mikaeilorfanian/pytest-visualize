import pytest
from pytest import fixture

from tree import TesstKlass, TesstFunction, TesstModule, TesstPackage, TreeRoot


class TestSamePackage:
    def test_add_module_to_package(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        assert test_package.json['isPackage'] is True
        assert test_package.json['name'] == 'tests'
        assert 'id' in test_package.json

    def test_add_same_module_twice(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)

        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        assert test_package.json['name'] == 'tests'

    def test_add_two_different_modules(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)

        test_module = test_package.get_or_create_module('tests/test_tesst_module2.py')
        assert isinstance(test_module, TesstModule)

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 2
        assert test_package.json['name'] == 'tests'

    def test_add_module_to_wrong_package(self):
        test_package = TesstPackage('tests')
        with pytest.raises(ValueError):
            test_package.get_or_create_module('tests1/test_tesst_module.py')


class TestTwoPackagesNested:
    def test_add_module_to_package(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1

        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'
        assert 'id' in sub_package

        test_module = sub_package['children'][0]
        assert test_module['name'] == 'test_tesst_module.py'
        assert test_module['isModule'] is True

    def test_add_same_module_twice(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

    def test_add_different_modules_to_same_sub_package(self):
        """
        package
           |
        package
          / \
    module  module
        """
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module1.py')
        assert isinstance(test_module, TesstModule)
        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 2
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

        module1 = sub_package['children'][0]
        assert module1['name'] == 'test_tesst_module.py'

        module2 = sub_package['children'][1]
        assert module2['name'] == 'test_tesst_module1.py'

    def test_add_modules_to_different_sub_packages(self):
        """
        package
          /  \
    package  package
      /        \
    module    module
        """
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'
        module = sub_package['children'][0]
        assert module['name'] == 'test_tesst_module.py'

        test_module = test_package.get_or_create_module('tests/tests2/test_tesst_module2.py')
        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 2
        sub_package = test_package.json['children'][1]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests2'
        module = sub_package['children'][0]
        assert module['name'] == 'test_tesst_module2.py'


class TestRootPackage:
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

    def test_add_module_within_package_and_root_level(self):
        tree = TreeRoot()
        tree.get_or_create_module('tests/test_sth.py')

        assert len(tree.json) == 1
        package = tree.json[0]
        assert package['name'] == 'tests'
        assert package['isPackage'] is True
        assert len(package['children']) == 1

        module = package['children'][0]
        assert module['name'] == 'test_sth.py'
        assert module['isModule'] is True
        assert len(module['children']) == 0

        tree.get_or_create_module('test_sth.py')
        assert len(tree.json) == 2
        root_module = tree.json[1]
        assert root_module['isModule'] is True
        assert root_module['name'] == 'test_sth.py'

    def test_add_module_within_nested_packages(self):
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


class TestMultipleLevelsOfNesting:
    def test_add_multiple_modules_at_different_levels_of_nesting(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')

        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1

        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'
        assert 'id' in sub_package

        test_module = sub_package['children'][0]
        assert test_module['name'] == 'test_tesst_module.py'
        assert test_module['isModule'] is True