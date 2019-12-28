from pytest import fixture

from tree import TesstKlass, TesstFunction, TesstMethod, TesstModule


@fixture
def function():  # TODO rename to `test_function`
    return TesstFunction(
        name='test_one',
        passed=True,
        node_id='test_sth.py::test_one',
        error=None,
        executed=True,
    )


@fixture
def function_two():
    return TesstFunction(
        name='test_two',
        passed=True,
        node_id='test_sth.py::test_two',
        error=None,
        executed=True,
    )


def test_add_function_to_module(function):
    module = TesstModule('test_sth.py', '')
    module.add_function(function)

    assert len(module.json['children']) == 1
    assert module.json['isModule'] is True
    assert module.json['name'] == 'test_sth.py'
    assert isinstance(module.json['id'], str)
    assert module.json['containsFailedTests'] is False

    func = module.json['children'][0]
    assert func['name'] == 'test_one'
    assert func['id'] == 'test_sth.py::test_one'
    assert func['isSingleTest'] is True


def test_add_two_functions_to_module(function, function_two):
    module = TesstModule('test_sth.py', '')
    module.add_function(function)
    module.add_function(function_two)

    assert len(module.json['children']) == 2
    assert module.json['isModule'] is True
    assert module.json['name'] == 'test_sth.py'
    assert isinstance(module.json['id'], str)
    assert module.json['containsFailedTests'] is False

    first_func = module.json['children'][0]
    assert first_func['name'] == 'test_one'
    assert first_func['id'] == 'test_sth.py::test_one'
    assert first_func['isSingleTest'] is True

    second_func = module.json['children'][1]
    assert second_func['name'] == 'test_two'
    assert second_func['id'] == 'test_sth.py::test_two'
    assert second_func['isSingleTest'] is True


@fixture
def failing_test_function():
    return TesstFunction(
        name='test_two',
        passed=False,
        node_id='test_sth.py::test_two',
        error=None,
        executed=True,
    )


def test_add_failing_test_function_to_module(failing_test_function):
    module = TesstModule('test_sth.py', '')
    module.add_function(failing_test_function)

    assert len(module.json['children']) == 1
    assert module.json['containsFailedTests'] is True


def test_add_a_mix_of_passing_and_failing_functions_to_module(failing_test_function, function):
    module = TesstModule('test_sth.py', '')
    module.add_function(failing_test_function)
    module.add_function(function)

    assert len(module.json['children']) == 2
    assert module.json['containsFailedTests'] is True


@fixture
def klass():
    return TesstKlass('TestKlass')


@fixture
def klass_two():
    return TesstKlass('TestKlass2')


def test_add_one_class():
    module = TesstModule('test_sth.py', '')
    assert module.json['containsFailedTests'] is False
    module.get_or_add_klass('TestKlass')

    assert len(module.json['children']) == 1
    assert module.json['containsFailedTests'] is False

    test_class = module.json['children'][0]
    assert test_class['name'] == 'TestKlass'
    assert test_class['isKlass'] is True


def test_add_two_classses():
    module = TesstModule('test_sth.py', '')
    module.get_or_add_klass('TestKlass')
    module.get_or_add_klass('TestKlass2')

    assert len(module.json['children']) == 2
    assert module.json['containsFailedTests'] is False

    first_klass = module.json['children'][0]
    assert first_klass['name'] == 'TestKlass'
    assert first_klass['isKlass'] is True

    second_klass = module.json['children'][1]
    assert second_klass['name'] == 'TestKlass2'
    assert second_klass['isKlass'] is True


def test_add_same_class_twice():
    module = TesstModule('test_sth.py', '')
    module.get_or_add_klass('TestKlass')
    module.get_or_add_klass('TestKlass')

    assert len(module.json['children']) == 1
    assert module.json['containsFailedTests'] is False

    test_class = module.json['children'][0]
    assert test_class['name'] == 'TestKlass'
    assert test_class['isKlass'] is True


@fixture
def failed_test_method():
    return TesstMethod(
        name='test_two',
        passed=False,
        node_id='test_sth.py::TestKlass::test_two',
        error='',
        executed=True,
    )


def test_add_klass_with_failing_test_to_module(failed_test_method):
    module = TesstModule('test_sth.py', '')
    klass = module.get_or_add_klass('TestKlass')
    klass.add_method(failed_test_method)

    assert module.json['containsFailedTests'] is True
