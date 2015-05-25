from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
import datetime
import ConfigParser
import os
import os.path
from secret_key import secret_key
import json

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
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	domain = db.Column(db.String(255), nullable=False)
	section_selector = db.Column(db.String(255), nullable=False)
	comment_selector = db.Column(db.String(255), nullable=False)
	template = db.Column(db.String(255), nullable=True, default='')
	category = db.Column(db.String(255), nullable=True, default='')
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	imported = db.Column(db.Boolean, default=False)

	def __init__(self, **kwargs):
		self.domain = kwargs['domain'][0]
		self.section_selector = kwargs['section_selector'][0]
		self.comment_selector = kwargs['comment_selector'][0]
		self.template = kwargs.get('template', '')[0]
		self.category = kwargs.get('category', '')[0]

	def json(self):
		return json.dumps({
			'domain' : self.domain,
			'section_selector' : self.section_selector,
			'comment_selector' : self.comment_selector,
			'template' : self.template,
			'category' : self.category
		}, sort_keys=False)

	def save(self):
		result = self.valid()
		if result['valid']:
			attempts = 0
			succeeded = False
			while attempts < 5:
				attempts += 1
				try:
					db.session.add(self)
					db.session.commit()
					succeeded = True
				except StandardError, ex:
					if ex.args[0] in (2006, 2013, 2055):
						continue
				break
		if succeeded:
			return result
		return {'valid' : False, 'error' : 'Database error, please try again later'}

	def valid(self):
		result = { "valid": True,
					"message" : ""}

		if len(self.domain) == 0:
			result['valid'] = False
			result['message'] += "Domain field is empty. "

		if len(self.section_selector) == 0:
			result['valid'] = False
			result['message'] += "Section selector field is empty. "

		if len(self.comment_selector) == 0:
			result['valid'] = False
			result['message'] += "Comment selector field is empty."

		return result

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

@app.route('/drtc/profile', methods=['POST'])
def profile():
	return drtc_controller.new_profile()

@app.route('/drtc/help')
def drtc_help():
	return drtc_controller.drtc_help()

@app.route('/drtc/donate')
def drtc_donate():
	return drtc_controller.drtc_donate()

@app.route('/drtc/profile_tutorial')
def drtc_profile_tutorial():
	return drtc_controller.drtc_profile_tutorial()

@app.route('/drtc/list_profiles')
def drtc_list_profiles():
	return drtc_controller.list_profiles()

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
