from flask import request, render_template
import flask_app
import logging

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_page(filename):
    return render_template('DRTC/' + filename + '.html')

def new_profile():
    profile = flask_app.Profile(**request.form)
    result = profile.save()
    if result['valid']:
        return 'Got it!'
    else:
        return result['message']

def profile_page():
    return render_template('DRTC/profile.html')
