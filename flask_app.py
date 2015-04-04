from flask import Flask, request, url_for, render_template, abort
import ConfigParser
from flask.ext.bootstrap import Bootstrap
import os
import os.path
from secret_key import secret_key
from drtc import DRTCController

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = secret_key

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
d = DRTCController()

@app.before_first_request
def config_read():
    c.readConfig()
    d.readConfig()

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

@app.route('/drtc')
def drtc():
    return d.drtc()

@app.route('/drtc/<filename>')
def drtc_page(filename):
    return d.drtc_page(filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/shutdown', methods=['GET'])
def shutdown():
    return c.shutdown()

# GNU Terry Pratchett
@app.after_request
def gnu_terry_pratchett(resp):
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp

if __name__ == '__main__':
    app.run(debug=config.getboolean('Controls', 'debug'))

