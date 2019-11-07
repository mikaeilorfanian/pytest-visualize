from flask import Flask
from flask import g
from flask_cors import CORS
import pytest


app = Flask(__name__)
CORS(app)


@app.route('/tests')
def collect_tests():
    g.collect_only = True
    pytest.main(['--collect-only'])
    return {'tests': g.tests}


@app.route('/tests/run')
def run_tests():
    g.run_tests = True
    pytest.main()
    return {'tests': g.tests}


@app.route('/tests/run/<node_id>')
def run_one_test(node_id):
    g.run_tests = True
    pytest.main([f'{node_id}'])
    return {'tests': g.tests}


app.run()
