from flask import request, render_template
import flask_app
import logging

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_profile_tutorial():
    return render_template('DRTC/profile_tutorial.html')

def new_profile():
    profile = flask_app.Profile(**request.form)
    result = profile.save()
    if result['valid']:
        return 'Your profile will be reviewed for a future release. Thanks!'
    else:
        return result['message']

def list_profiles():
	profiles = flask_app.Profile.query.filter_by(imported=False).all()
	profiles_json = []

	for p in profiles:
		profiles_json.append(p.json())

	return render_template('DRTC/profile_list.html', profiles=profiles_json)

