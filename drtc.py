from flask import request, render_template, redirect
import flask_app

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_page(filename):
    return render_template('DRTC/' + filename + '.html')

def new_profile():
    try:
        profile = flask_app.Profile(**request.form)
        profile.save()
        return 'Got it!'
    except:
        return 'Some shit happened'

def profile_page():
    return render_template('DRTC/profile.html')
