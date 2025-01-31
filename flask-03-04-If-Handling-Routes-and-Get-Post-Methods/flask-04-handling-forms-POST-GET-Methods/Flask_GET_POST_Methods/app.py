# Import Flask modules
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')



# Create an object named app



# create a function named "lcm" which calculates a least common multiple values of two numbers. 



# Create a function named `index` which uses template file named `index.html` 
# send two numbers as template variable to the app.py and assign route of no path ('/') 





# calculate sum of them using "lcm" function, then sent the result to the 
# "result.hmtl" file and assign route of path ('/calc'). 
# When the user comes directly "/calc" path, "Since this is a GET request, LCM has not been calculated" string returns to them with "result.html" file


@app.route('/calc',methods=['GET','POST'])
def calc():
    if request.method == 'POST':
        num1=request.form.get('number1')
        num2=request.form.get('number2')
        result=int(num1)*int(num2)
        return render_template('result.html',a=num1,b=num2,result=result,developer_name="Steve")
    else:
        return render_template('result.html',developer_name="Steve")



# Add a statement to run the Flask application which can be debugged.
if __name__ == '__main__':
    app.run(debug=True,port=5002)
