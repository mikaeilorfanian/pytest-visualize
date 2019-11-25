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

        if 'tests' not in g:
            g.tests = defaultdict(list)

    except RuntimeError:
        if report.when == 'call':
            print(Path(report.location[0]).parts)
            print(type(report.location[0]))
        return



    if report.when == 'call':
        tree.add_test_to_test_tree(report, g)

        test = {
            'name': report.location[2],
            'passed': report.passed,
            'nodeId': report.nodeid,
        }

        if not report.passed:
            test['errorLog'] = str(report.longrepr)

        g.tests[report.location[0]].append(test)


def pytest_collection_finish(session):
    try:
        if 'collect_only' not in g or not g.collect_only:
            return
   
        if 'collected_tests' not in g:
            g.collected_tests = defaultdict(list)
    except RuntimeError:
        for item in session.items:
            # print(item.nodeid, type(item.nodeid))
            # print(item.location)
            break
            # print(item.name, type(item.name))
        return

    for item in session.items:
        g.collected_tests[item.location[0]].append(
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