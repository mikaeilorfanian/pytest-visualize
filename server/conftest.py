from collections import defaultdict
from pprint import pprint

from flask import g

# def pytest_runtest_setup(item):
#     pprint(item.name)

def pytest_report_teststatus(report, config):
    # pprint(report.passed)
    # pprint(report.when)
    if 'run_tests' not in g or not g.run_tests:
        return

    try:
        if 'tests' not in g:
            g.tests = defaultdict(list)
    except RuntimeError:
        print(report.when)
        return

    if report.when == 'call':
        g.tests[report.location[0]].append(
            {
                'name': report.location[2], 
                'passed': report.passed,
                'nodeId': report.nodeid,
            }
        )


def pytest_collection_finish(session):
    if 'collect_only' not in g or not g.collect_only:
        return

    try:
        if 'tests' not in g:
            g.tests = defaultdict(list)
    except RuntimeError:
        for item in session.items:
            # print(item.nodeid, type(item.nodeid))
            print(item.location)
            break
            # print(item.name, type(item.name))
        return

    for item in session.items:
        g.tests[item.location[0]].append(
            {
                'name': item.name, 
                # 'passed': report.passed,
                'nodeId': item.nodeid,
            }
        )
    # print(dir(session))
    # print(session.items)
    # for item in session.items:
    #     print(item.nodeid, type(item.nodeid))
    #     print(item.module)
    #     print(item.name, type(item.name))
        # print(dir(item))