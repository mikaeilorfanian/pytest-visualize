from collections import defaultdict
from pathlib import Path
from pprint import pprint

from flask import g

import tree

# def pytest_runtest_setup(item):
#     pprint(item.name)

def pytest_report_teststatus(report, config):
    # pprint(report.passed)
    # pprint(report.when)
    try:
        if 'run_tests' not in g or not g.run_tests:
            return
    except RuntimeError:
        if report.when == 'call':
            pass
            # print(Path(report.location[0]).parts)
            # print(type(report.location[0]))
        return

    if report.when == 'call':
        tree.add_test_to_test_tree(report, g)


def pytest_collection_finish(session):
    try:
        if 'collect_only' not in g or not g.collect_only:
            return

    except RuntimeError:
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

        tree.add_test_to_test_tree(item, g, test_executed=False)
    # print(dir(session))
    # print(session.items)
    # for item in session.items:
    #     print(item.nodeid, type(item.nodeid))
    #     print(item.module)
    #     print(item.name, type(item.name))
        # print(dir(item))