from flask import request, render_template, redirect

def drtc():
    return render_template('DRTC/drtc.html')

def drtc_page(filename):
    return render_template('DRTC/' + filename + '.html')

def new_profile():
    from flask_app import app
    app.logger.warning(request.form)
    # return redirect('/drtc')
    return 'Got it!'

def profile_page():
    print 'GET'
    return redirect('/drtc')