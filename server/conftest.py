from flask import g
import _pytest

import tree


TEST_EXECUTED = 'call'


def pytest_report_teststatus(report, config):
    """
    This function in invoked by pytest during the processing of each test.
    We're only interested in the "call" report, which comes after a test has been executed.
    Using flask's `g` object, we build a test tree which is returned to front-end.
    """
    # pprint(report.passed)
    # pprint(report.when)
    try:
        if 'run_tests' not in g or not g.run_tests:
            return
    except RuntimeError:  # when pytest is invoked outside flask's app context
        if report.when == TEST_EXECUTED:
            pass
        return

    if report.when == TEST_EXECUTED:
        tree.add_test_to_test_tree(report, g)


def pytest_collection_finish(session):
    """
    This function in invoked by pytest after test collection is done.
    Using flask's `g` object, we build a test tree which is returned to front-end.
    """
    try:
        if 'collect_only' not in g or not g.collect_only:
            return

    except RuntimeError:  # when pytest is invoked outside flask's app context
        for item in session.items:
            break
        return

    for item in session.items:
        tree.add_test_to_test_tree(item, g, was_executed=False)


def pytest_exception_interact(node: _pytest.python.Module, call: _pytest.runner.CallInfo, report):
    try:
        g.user_code_error = node.repr_failure(call.excinfo)
    except RuntimeError:
        pass
