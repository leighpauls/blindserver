from flask import Flask, escape, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!\n'

@app.route('/healthz')
def healthz():
    return 'OK'

@app.route('/fulfill', methods=['POST'])
def fulfill():
    body = request.json
    request_id = body['requestId']
    first_input = body['inputs'][0]
    intent = first_input['intent']
    output_payload = {}

    if intent == 'action.devices.SYNC':
        output_payload = {
            'agentUserId': 'leigh',
            'devices': [{
                'id': 'blinds',
                'type': 'action.devices.types.BLINDS',
                'traits': ['action.devices.traits.OpenClose'],
                'name': {
                    'name': 'blinds',
                    'nicknames': ['living room blinds'],
                },
                'willReportState': False,
                'attributes': {
                    'discreteOnlyOpenClose': True,
                },
            }]
        }
    elif intent == 'action.devices.EXECUTE':
        input_payload = first_input['payload']
        commands = input_payload['commands']
        output_commands = []
        for command in commands:
            executions = command['execution']
            for execution in executions:
                cmd = execution['command']
                params = execution['params']
                print(f'Command: {cmd} with param: {params}')
                should_open = params['openPercent'] == 100
                send_blinds_message(should_open)
            device_ids = [device['id'] for device in command['devices']]
            output_commands.append({'ids': device_ids, 'status': 'SUCCESS'})
        output_payload = {
            'commands': output_commands
        }
    else:
        raise Exception(f'Unexpected intent: {intent}')

    result = {
        'requestId': request_id,
        'payload': output_payload,
    }

    return json.dumps(result)

def send_blinds_message(should_open: bool):
    client = mqtt.Client('command_server')
    client.connect('localhost')
    message_info = client.publish('/blinds', payload=json.dumps({'should_open': should_open}), qos=0)
    message_info.wait_for_publish()

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

