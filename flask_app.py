
from flask import Flask, request, url_for, render_template, abort
import random
import ConfigParser
from flask.ext.bootstrap import Bootstrap
import os
import os.path

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'This is really unique and secret'

class IndexController(object):

    def __init__(self):
        self.config = None

    def readConfig(self):
        if not self.config:
            self.config = ConfigParser.SafeConfigParser()
            self.filepath = os.path.join(os.getcwd(), 'coldbrew.cfg')
            self.config.read(self.filepath)

    def index(self):
        return render_template('index.html')

    def about(self):
        return render_template('about.html')

    def resume(self):
        return render_template('resume.html')

    def eriu(self):
        return render_template('eriu.html')

    def drtc(self, filename):
        return render_template('DRTC/' + filename + '.html')

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def shutdown(self):
        if self.config.getboolean('Controls', 'shutdown'):
            self.shutdown_server()
            return 'Server shutting down...'
        return self.index()

c = IndexController()

@app.before_first_request
def config_read():
    c.readConfig()

@app.route('/')
def index():
    return c.index()

@app.route('/about')
def about():
    return c.about()

@app.route('/resume')
def resume():
    return c.resume()

@app.route('/eriu')
def eriu():
    return c.eriu()

@app.route('/barracuda-site-verification-2d21942148aa9505b3db97c56407de97.html')
def verification():
    return '2d21942148aa9505b3db97c56407de97', 200

@app.route('/drtc/<filename>')
def drtc(filename):
    return c.drtc(filename)

@app.errorhandler(404) 
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/shutdown', methods=['GET'])
def shutdown():
    return c.shutdown()



if __name__ == '__main__':
    app.run(debug=True)
