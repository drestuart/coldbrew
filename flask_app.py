from flask import Flask, request, url_for, render_template
import random
# from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
# manager = Manager(app)
bootstrap = Bootstrap(app)
app.secret_key = 'This is really unique and secret'

@app.route('/')
def hello_person():
    return """
        <title>Coldbrew Games</title>
        <p>What is this, a game company for ants?</p>
        <form method="POST" action="%s"><input name="person" /><input type="submit" value="Go!" /></form>
        """ % (url_for('greet'),)

@app.route('/greet', methods=['POST'])
def greet():
    greeting = random.choice(["Hiya", "Hallo", "Hola", "Ola", "Salut", "Privet", "Konnichiwa", "Ni hao"])
    return """
        <title>Coldbrew Games</title>
        <p>%s, %s!</p>
        <p><a href="%s">Back to start</a></p>
        """ % (greeting, request.form["person"], url_for('hello_person'))
        
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
