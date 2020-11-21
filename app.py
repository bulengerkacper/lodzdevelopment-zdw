from flask import Flask, render_template, redirect
from flask import request
from utils import calc

application = Flask(__name__)

@application.route("/")
def main():
    return render_template("index.html")

@application.route('/test')  
def home():
    return calc.test()

@application.route('/form', methods=['GET', 'POST'])  
def form_collector():
    return "nothing to discuss"

if __name__ == "__main__":
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run(debug=True, host='127.0.0.1')
