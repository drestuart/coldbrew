from flask import Flask, request, url_for, render_template
import random
# from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)
app.secret_key = 'This is really unique and secret'

@app.route('/')
def index():
    return render_template('index.html')
#     return """
#         <title>Coldbrew Games</title>
#         <p>What is this, a game company for ants?</p>
#         <form method="POST" action="%s"><input name="person" /><input type="submit" value="Go!" /></form>
#         """ % (url_for('greet'),)

@app.route('/about')
def about():
    return render_template('about.html')
        
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
        
if __name__ == '__main__': 
    app.run(debug=True)
