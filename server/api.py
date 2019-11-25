from flask import Flask, jsonify
from flask import g
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO
import pytest


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:8080'])  # the IP of local front-end server


@app.route('/tests')
def collect_tests():
    g.collect_only = True
    pytest.main(['--collect-only'])
    return {'collectedTestsTree': g.collected_tests_tree.json}


@app.route('/tests/run', methods=['GET', 'POST'])
def run_tests():
    g.run_tests = True
    g.collect_only = True

    if request.method == 'GET':  # call for running all tests
        pytest.main()
        return {'collectedTestsTree': g.collected_tests_tree.json, 'executedTestsTree': g.tests_tree.json}
    
    test_node_ids = request.json

    if not isinstance(test_node_ids, list) or len(test_node_ids) < 1:
        return {'error': 'Test node IDs should be in JSON body of request!'}
    
    bad_test_node_ids = list(filter(lambda test_node_id: test_node_id is None, test_node_ids))
    if bad_test_node_ids:
        return {'error': 'Invalid test node ID'}

    pytest.main([node['id'] for node in test_node_ids])

    if 'tests_tree' not in g or 'collected_tests_tree' not in g:
        return {'error': 'Collect tests again, tests are out of sync!'}

    # try:
    #     if len(test_node_ids) != len(g.tests):
    #         return {'error': f'Collect tests again! They are out of sync, one or more didnt run! Requested {len(test_node_ids)} ran {len(g.collected_tests)}'}
    # except AttributeError:
    #     return {'error': 'Collect tests again! They are out of sync, one or more not found!'}

    return {'collectedTestsTree': g.collected_tests_tree.json, 'executedTestsTree': g.tests_tree.json}


# @app.route('/tests/run/<node_id>')
# def run_one_test(node_id):
#     g.run_tests = True
#     pytest.main([f'{node_id}'])
#     return {'tests': g.tests}
if __name__ == '__main__':
    socketio.run(app)
