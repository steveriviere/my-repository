from flask import Flask 
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/bye')
def bye():
    return 'Bye!'


@app.route('/my/sub')
def sub():
    return 'my subfolder '

@app.route('/test/<string:id>')
def test(id):
    output = f"my output is {id}"
    return output




if __name__ == '__main__':

    app.run(debug=True, port=5000)
    # app.run(host= '0.0.0.0', port=8081)