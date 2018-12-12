import os

from flask import abort, Flask, jsonify, request


app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@app.route('/auth-ok', methods=['POST'])
def auth_ok():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        status=200,
        text='Ok',
    )

@app.route('/ok', methods=['GET', 'POST'])
def ok(): 
    print(request.form['team_domain'])
    return jsonify(
        status=200,
        text='Ok',
    )