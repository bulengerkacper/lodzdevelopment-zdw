from flask import Flask, render_template, redirect
from flask import request

application = Flask(__name__)

@application.route("/")
def main():
    return render_template("index.html")

if __name__ == "__main__":
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run(debug=True, host='0.0.0.0')
