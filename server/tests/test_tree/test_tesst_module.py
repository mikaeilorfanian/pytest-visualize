from pytest import fixture

from tree import TesstKlass, TesstFunction, TesstModule


@fixture
def function():
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
    module = TesstModule('test_sth.py')
    module.add_function(function)

    assert len(module.json['children']) == 1
    assert module.json['isModule'] is True
    assert module.json['name'] == 'test_sth.py'
    assert isinstance(module.json['id'], int)

    func = module.json['children'][0]
    assert func['name'] == 'test_one'
    assert func['id'] == 'test_sth.py::test_one'
    assert func['isSingleTest'] is True


def test_add_two_functions_to_module(function, function_two):
    module = TesstModule('test_sth.py')
    module.add_function(function)
    module.add_function(function_two)

    assert len(module.json['children']) == 2
    assert module.json['isModule'] is True
    assert module.json['name'] == 'test_sth.py'
    assert isinstance(module.json['id'], int)

    func = module.json['children'][0]
    assert func['name'] == 'test_one'
    assert func['id'] == 'test_sth.py::test_one'
    assert func['isSingleTest'] is True

    func = module.json['children'][1]
    assert func['name'] == 'test_two'
    assert func['id'] == 'test_sth.py::test_two'
    assert func['isSingleTest'] is True


@fixture
def klass():
    return TesstKlass('TestKlass')


@fixture
def klass_two():
    return TesstKlass('TestKlass2')


def test_add_one_class():
    module = TesstModule('test_sth.py')
    module.get_or_add_klass('TestKlass')

    assert len(module.json['children']) == 1

    test_class = module.json['children'][0]
    assert test_class['name'] == 'TestKlass'
    assert test_class['isKlass'] is True


def test_add_two_classses():
    module = TesstModule('test_sth.py')
    module.get_or_add_klass('TestKlass')
    module.get_or_add_klass('TestKlass2')

    assert len(module.json['children']) == 2

    test_class = module.json['children'][0]
    assert test_class['name'] == 'TestKlass'
    assert test_class['isKlass'] is True

    test_class = module.json['children'][1]
    assert test_class['name'] == 'TestKlass2'
    assert test_class['isKlass'] is True


def test_add_same_class_twice():
    module = TesstModule('test_sth.py')
    module.get_or_add_klass('TestKlass')
    module.get_or_add_klass('TestKlass')

    assert len(module.json['children']) == 1

    test_class = module.json['children'][0]
    assert test_class['name'] == 'TestKlass'
    assert test_class['isKlass'] is True