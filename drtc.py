from flask import request, render_template, redirect
from flask_app import Profile

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_page(filename):
    return render_template('DRTC/' + filename + '.html')

def new_profile():
    try:
        profile = Profile(**request.form)
        profile.save()
        return 'Got it!'
    except:
        return 'Some shit happened'

def profile_page():
    return render_template('DRTC/profile.html')
