from flask import Flask
from flask import g
from flask import request
from flask_cors import CORS
import pytest


app = Flask(__name__)
CORS(app)


@app.route('/tests')
def collect_tests():
    g.collect_only = True
    pytest.main(['--collect-only'])
    return {'tests': g.tests}


@app.route('/tests/run', methods=['GET', 'POST'])
def run_tests():
    g.run_tests = True
    
    if request.method == 'GET':    
        pytest.main()
        return {'tests': g.tests}
    
    test_node_ids = request.json
    print(test_node_ids)
    if not isinstance(test_node_ids, list) or len(test_node_ids) < 1:
        return {'error': 'Test node IDs should be in JSON body of request!'}, 400
    
    bad_test_node_ids = list(filter(lambda test_node_id: test_node_id is None, test_node_ids))
    if bad_test_node_ids:
        return {'error': 'Invalid test node ID'}, 400

    pytest.main([test_node_ids[0]['id']])  # TODO run multiple tests
    return {'tests': g.tests}

# @app.route('/tests/run/<node_id>')
# def run_one_test(node_id):
#     g.run_tests = True
#     pytest.main([f'{node_id}'])
#     return {'tests': g.tests}


app.run()
