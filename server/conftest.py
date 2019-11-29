from collections import defaultdict
from pathlib import Path
from pprint import pprint

from flask import g

import tree


TEST_EXECUTED = 'call'

# def pytest_runtest_setup(item):
#     pprint(item.name)

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
            # print(Path(report.location[0]).parts)
            # print(type(report.location[0]))
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
            # print(item.nodeid, type(item.nodeid))
            # print(item.location)
            break
            # print(item.name, type(item.name))
        return

    for item in session.items:
        # print(item.location[0])
        # print(item.name)
        # print(item.location[2])
        # print(item.nodeid)

        tree.add_test_to_test_tree(item, g, was_executed=False)
    # print(dir(session))
    # print(session.items)
    # for item in session.items:
    #     print(item.nodeid, type(item.nodeid))
    #     print(item.module)
    #     print(item.name, type(item.name))
        # print(dir(item))