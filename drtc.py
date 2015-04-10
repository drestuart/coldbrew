from flask import request, render_template
import flask_app
import logging

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_page(filename):
    return render_template('DRTC/' + filename + '.html')

def new_profile():
    try:
        profile = flask_app.Profile(**request.form)
        result = profile.save()
        if result['valid']:
            return 'Got it!'
        else:
            return result['message']
    except Exception as e:
        logging.warning(e)
        return 'Some shit happened'

def profile_page():
    return render_template('DRTC/profile.html')
