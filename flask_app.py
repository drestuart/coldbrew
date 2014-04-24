from flask import Flask, request, url_for
import random

app = Flask(__name__)
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
