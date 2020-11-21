from flask import Flask, render_template, redirect
from flask import request
import json
from utils import calc

application = Flask(__name__)

@application.route("/")
def main():
    return render_template("index.html")

@application.route('/test')  
def test():
    with open('data/input.json') as src:
        data = json.load(src)
    return calc.do_calc(data)


@application.route('/calc', methods = ['POST'])
def calculate():
    if request.method == 'POST':
        data = request.get_json()
        return calc.do_calc(data)

@application.route('/gas_network')
def gas_network():
    file = open("utils/json_generator_for_maps/siec_gazowa.txt.jsons")  
    return file.read()

@application.route('/heat_network')
def heat_network():
    file = open("utils/json_generator_for_maps/siec_cieplownicza.txt.jsons")  
    return file.read()

    

@application.route('/form', methods=['GET', 'POST'])  
def form_collector():
    return "nothing to discuss"

if __name__ == "__main__":
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run(debug=True, host='127.0.0.1')
