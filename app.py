from flask import Flask, escape, request
import json

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!\n'

@app.route('/healthz')
def healthz():
    return 'OK'

@app.route('/fulfill')
def fulfill():
    return 'OK'

@app.route('/auth')
def auth():
    redirect_uri = request.args['redirect_uri']
    state = request.args['state']
    code = '1234poop'
    return f'<a href="{redirect_uri}?code={code}&state={state}">OK</a>'

@app.route('/token', methods=['POST'])
def token():
    result = {
        'token_type': 'Bearer',
        'access_token': 'someAccessToken',
        'expires_in': 43200
    }

    if request.form['grant_type'] == 'authorization_code':
        result['refresh_token'] = 'someRefreshToken'
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

