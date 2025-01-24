from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def head():
    return render_template("index.html",number1=10, number2=20)


@app.route('/<string:number1>/<string:number2>')
def number(number1, number2):
    return render_template("index.html",number1=number1, number2=number2)

@app.route('/sum/<string:number1>/<string:number2>')
def sum(number1, number2):
    if number1.isdigit() and number2.isdigit():
        value1=int(number1)
        value2=int(number2)
        sum=value1+value2
        return render_template("body.html",value1=value1, value2=value2,sum=sum)
    else:
        return "poorly formatted url"






if __name__== "__main__":
    app.run(debug=True, port=5001)
    # app.run(host= '0.0.0.0', port=8081)