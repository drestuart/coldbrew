
from flask import Flask, request, url_for, render_template
import random
import ConfigParser
from flask.ext.bootstrap import Bootstrap
import os
import os.path

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)
app.secret_key = 'This is really unique and secret'

config = ConfigParser.SafeConfigParser()
filepath = os.path.join(os.getcwd(), 'coldbrew.cfg')
#config.read(filepath)
config.read('coldbrew.cfg.bk')

@app.route('/')
def index():

    stuff = filepath + "<br>"
    stuff += os.getcwd()

    #file = open(filepath)
    #stuff += file.read() + "<br>"
    #file.close()

    return stuff + render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/eriu')
def eriu():
    return render_template('eriu.html')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    if config.getboolean('Controls', 'shutdown'):
        shutdown_server()
        return 'Server shutting down...'
    return index()

if __name__ == '__main__':
    app.run(debug=True)
