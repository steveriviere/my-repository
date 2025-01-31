# Import Flask modules
from flask import Flask, render_template

from rich.markup import render

# Create an object named app
app=Flask(__name__)



# Create a function named head which shows the massage as "This is my first conditions experience" in `index.html` 
# and assign to the route of ('/')
@app.route('/')
def head():
    first="this is my first experience"
    return render_template("index.html",message=first)


# Create a function named list_names which prints names elements of list one by one in `index.html`
# and assign to the route of ('/')

@app.route('/list')
def list_names():
    mynames=["Steve","Abelarde","Jonathan"]
    return render_template("body.html",object=mynames)



# run this app in debug mode on your local.

if __name__=='__main__':
    app.run(debug=True)
