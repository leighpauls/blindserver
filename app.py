from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!\n'

@app.route('/healthz')
def healthz():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
