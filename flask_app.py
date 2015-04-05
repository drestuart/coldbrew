from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
import ConfigParser
import os
import os.path
from secret_key import secret_key

# Read config file
config = ConfigParser.SafeConfigParser()
filepath = os.path.join(os.getcwd(), 'coldbrew.cfg')
config.read(filepath)

app = Flask(__name__)
app.secret_key = secret_key
bootstrap = Bootstrap(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://' + config.get('Database', 'username') + ':' \
    + config.get('Database', 'password') + '@' + config.get('Database', 'hostname') \
    + '/' + config.get('Database', 'database')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# Import controllers and models
import drtc as drtc_controller

class Profile(db.Model):
    __tablename__ = 'drtc_profiles'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    section_selector = db.Column(db.String(255), nullable=False)
    comment_selector = db.Column(db.String(255), nullable=False)
    template = db.Column(db.String(255), nullable=True, default='')
    category = db.Column(db.String(255), nullable=True, default='')

    def __init__(self, **kwargs):
        self.domain = kwargs['domain']
        self.section_selector = kwargs['section_selector']
        self.comment_selector = kwargs['comment_selector']
        self.template = kwargs.get('template', '')
        self.category = kwargs.get('category', '')

    def save(self):
        db.session.add(self)
        db.session.commit()

# Main Site

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/eriu')
def eriu():
    return render_template('eriu.html')

# DRTC

@app.route('/drtc')
def drtc():
    return drtc_controller.drtc()

@app.route('/drtc/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        return drtc_controller.new_profile()
    else:
        return drtc_controller.profile_page()

@app.route('/drtc/<filename>')
def drtc_page(filename):
    return drtc_controller.drtc_page(filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/shutdown', methods=['GET'])
def shutdown():
    if config.getboolean('Controls', 'shutdown'):
        shutdown_server()
        return 'Server shutting down...'
    return index()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# GNU Terry Pratchett
@app.after_request
def gnu_terry_pratchett(resp):
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp

if __name__ == '__main__':
    # Create DB tables
    db.create_all()
    db.session.commit()

    app.run(debug=config.getboolean('Controls', 'debug'))
