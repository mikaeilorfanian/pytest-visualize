import os

from flask import Flask, jsonify
from flask import g
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO
import pytest

from errors import UserCodeException


CORS_IP = os.environ.get('CORS_IP') or 'http://localhost:8080'  # the IP of local front-end server


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=[CORS_IP])


@app.errorhandler(UserCodeException)
def handle_error(error):
    return jsonify(error.json)


@app.route('/tests')
def collect_tests():
    g.collect_only = True
    pytest.main(['--collect-only'])

    if 'user_code_error' in g:
        raise UserCodeException(g.user_code_error)

    return {
        'collectedTestsTree': g.collected_tests_tree.json,
        'collectedTestsCount': g.collected_tests_counter,
    }


@app.route('/collected_tests')
def collected_tests():
    g.collect_only = True
    pytest.main(['--collect-only'])

    if 'user_code_error' in g:
        raise UserCodeException(g.user_code_error)

    return {
        'collectedTestsTree': g.collected_tests_tree.json_paths_only,
        'collectedTestsCount': g.collected_tests_counter,
    }


@app.route('/tests/run', methods=['GET', 'POST'])
def run_tests():
    g.run_tests = True
    g.collect_only = True

    if request.method == 'GET':  # call for running all tests
        pytest.main()

        if 'tests_tree' not in g or 'collected_tests_tree' not in g:
            if 'user_code_error' in g:
                raise UserCodeException(g.user_code_error)

        return {
            'collectedTestsTree': g.collected_tests_tree.json,
            'executedTestsTree': g.tests_tree.json,
            'failedTests': g.failed_tests,
            'executedTestsCount': g.executed_tests_counter,
        }
    
    test_node_ids = request.json

    if not isinstance(test_node_ids, list) or len(test_node_ids) < 1:
        return {'error': 'Test node IDs should be in JSON body of request!'}
    
    bad_test_node_ids = list(filter(lambda test_node_id: test_node_id is None, test_node_ids))
    if bad_test_node_ids:
        return {'error': 'Invalid test node ID'}

    pytest.main([node['id'] for node in test_node_ids])

    if 'tests_tree' not in g or 'collected_tests_tree' not in g:
        if 'user_code_error' in g:
            raise UserCodeException(g.user_code_error)

        return {'error': 'Collect tests again, tests are out of sync!'}

    try:
        if len(test_node_ids) != g.executed_tests_counter:
            return {
                'error': f'Collect tests again! '
                f'They are out of sync, one or more didnt run! '
                f'Requested {len(test_node_ids)} ran {g.executed_tests_counter}'}
    except AttributeError:
        return {'error': 'Collect tests again! They are out of sync, one or more not found!'}

    return {
        'collectedTestsTree': g.collected_tests_tree.json,
        'executedTestsTree': g.tests_tree.json,
        'failedTests': g.failed_tests,
        'executedTestsCount': g.executed_tests_counter,
    }


# @app.route('/tests/run/<node_id>')
# def run_one_test(node_id):
#     g.run_tests = True
#     pytest.main([f'{node_id}'])
#     return {'tests': g.tests}
if __name__ == '__main__':
    socketio.run(app)
