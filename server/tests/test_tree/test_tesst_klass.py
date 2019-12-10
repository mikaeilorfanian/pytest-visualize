from pytest import fixture

from tree import TesstKlass, TesstMethod


@fixture
def method():  # TODO rename this to `test_method`
    return TesstMethod(
        name='test_one',
        passed=True,
        node_id='test_sth.py::TestKlass::test_one',
        error='',
        executed=True,
    )


@fixture
def method_two():
    return TesstMethod(
        name='test_two',
        passed=True,
        node_id='test_sth.py::TestKlass::test_two',
        error='',
        executed=True,
    )


def test_add_one_method(method):
    klass = TesstKlass('TestKlass')
    klass.add_method(method)

    assert klass.json['isKlass'] is True
    assert klass.json['containsFailedTests'] is False
    assert klass.json['id'] == klass.name
    assert klass.json['name'] == 'TestKlass'
    assert len(klass.json['children']) == 1

    test_method = klass.json['children'][0]
    assert test_method['name'] == 'test_one'
    assert test_method['id'] == 'test_sth.py::TestKlass::test_one'
    assert test_method['isSingleTest'] is True
    assert test_method['wasExecuted'] is True
    assert test_method['passed'] is True
    assert test_method['errorRepr'] is ''


def test_add_two_methods(method, method_two):
    klass = TesstKlass('TestKlass')
    klass.add_method(method)
    klass.add_method(method_two)

    assert len(klass.json['children']) == 2
    assert klass.json['containsFailedTests'] is False

    first_method = klass.json['children'][0]
    assert first_method['name'] == 'test_one'
    assert first_method['id'] == 'test_sth.py::TestKlass::test_one'
    assert first_method['isSingleTest'] is True
    assert first_method['wasExecuted'] is True
    assert first_method['passed'] is True
    assert first_method['errorRepr'] is ''

    second_method = klass.json['children'][1]
    assert second_method['name'] == 'test_two'
    assert second_method['id'] == 'test_sth.py::TestKlass::test_two'


@fixture
def failed_test_method():
    return TesstMethod(
        name='test_two',
        passed=False,
        node_id='test_sth.py::TestKlass::test_two',
        error='',
        executed=True,
    )


def test_add_failed_test_to_klass(failed_test_method):
    klass = TesstKlass('TestKlass')
    klass.add_method(failed_test_method)

    assert len(klass.json['children']) == 1
    assert klass.json['containsFailedTests'] is True


def test_add_passed_and_failed_tests(method, failed_test_method):
    klass = TesstKlass('TestKlass')
    klass.add_method(failed_test_method)
    klass.add_method(method)

    assert len(klass.json['children']) == 2
    assert klass.json['containsFailedTests'] is True
