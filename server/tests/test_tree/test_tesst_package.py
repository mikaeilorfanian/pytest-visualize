import pytest
from pytest import fixture

from tree import TesstKlass, TesstFunction, TesstMethod, TesstModule, TesstPackage, TreeRoot


@fixture
def failed_test_method():
    return TesstMethod(
        name='test_two',
        passed=False,
        node_id='test_sth.py::TestKlass::test_two',
        error='',
        executed=True,
    )


class TestSamePackage:
    def test_add_module_to_package(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')

        assert isinstance(test_module, TesstModule)
        assert len(test_package.json['children']) == 1
        assert test_package.json['isPackage'] is True
        assert test_package.json['name'] == 'tests'
        assert 'id' in test_package.json
        assert test_package.json['containsFailedTests'] is False

    def test_failing_module_to_package(self, failed_test_method):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        klass = test_module.get_or_add_klass('TestKlass')
        klass.add_method(failed_test_method)

        assert test_package.json['containsFailedTests'] is True

    def test_add_same_module_twice(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)

        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)

        assert len(test_package.json['children']) == 1
        assert test_package.json['name'] == 'tests'

        assert test_package.json['containsFailedTests'] is False

    def test_add_two_different_modules(self):
        test_package = TesstPackage('tests')
        first_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        assert isinstance(first_module, TesstModule)

        second_module = test_package.get_or_create_module('tests/test_tesst_module2.py')
        assert isinstance(second_module, TesstModule)

        assert len(test_package.json['children']) == 2
        assert test_package.json['name'] == 'tests'

    def test_add_failing_and_passing_modules(self, failed_test_method):
        test_package = TesstPackage('tests')
        test_package.get_or_create_module('tests/test_tesst_module.py')

        assert test_package.json['containsFailedTests'] is False

        test_module = test_package.get_or_create_module('tests/test_tesst_module.py')
        klass = test_module.get_or_add_klass('TestKlass')
        klass.add_method(failed_test_method)

        assert test_package.json['containsFailedTests'] is True

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
        assert test_package.json['containsFailedTests'] is False

        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'
        assert 'id' in sub_package
        assert sub_package['containsFailedTests'] is False

        test_module = sub_package['children'][0]
        assert test_module['name'] == 'test_tesst_module.py'
        assert test_module['isModule'] is True

    def test_add_same_module_twice(self):
        test_package = TesstPackage('tests')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        assert test_module.json['name'] == 'test_tesst_module.py'
        assert len(test_package.json['children']) == 1

        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(test_module, TesstModule)
        assert test_module.json['name'] == 'test_tesst_module.py'

        # make sure no more packages or sub-packages were added
        assert len(test_package.json['children']) == 1

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
        first_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        assert isinstance(first_module, TesstModule)
        assert len(test_package.json['children']) == 1

        sub_package = test_package.json['children'][0]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests1'

        module = sub_package['children'][0]
        assert module['name'] == 'test_tesst_module.py'

        second_module = test_package.get_or_create_module('tests/tests2/test_tesst_module2.py')
        assert isinstance(second_module, TesstModule)
        assert len(test_package.json['children']) == 2

        sub_package = test_package.json['children'][1]
        assert len(sub_package['children']) == 1
        assert sub_package['isPackage'] is True
        assert sub_package['name'] == 'tests2'

        module = sub_package['children'][0]
        assert module['name'] == 'test_tesst_module2.py'


class TestMultipleLevelsOfNesting:
    def test_add_multiple_modules_at_different_levels_of_nesting(self, failed_test_method):
        test_package = TesstPackage('tests')
        test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        test_module = test_package.get_or_create_module('tests/tests1/test_tesst_module.py')
        klass = test_module.get_or_add_klass('TestKlass')
        klass.add_method(failed_test_method)

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

        assert test_package.json['containsFailedTests'] is True