import os
import base64
import random
import string
import sys

from flask import Flask, request, session
from model import Grade 

app = Flask(__name__)
app.secret_key = b'\x98E\xb3\xb4O\xd9\xd8\xf7\xe1C\x89\xef\x89\xc2G\xd6\xa9W\x84\xc2hCP\xfb'

@app.route('/', methods=['GET', 'POST'])
def home():
    #Added

    if 'csrf_token' not in session:
        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(10))
        session['csrf_token'] = key 
        
    if request.method == 'POST':
        if request.form.get('csrf_token', None) == session['csrf_token']:   #Added
            g = Grade(
                student=request.form['student'],
                assignment=request.form['assignment'],
                grade=request.form['grade'],
            )
            #print("(" + request.form['grade'] + ")")
            g.save()

    body = """
<html>
<body>
<h1>Enter Grades</h1>
<h2>Enter a Grade</h2>
<form method="POST">
    <label for="student">Student</label>
    <input type="text" name="student"><br>


    <label for="assignment">Assignment</label>
    <input type="text" name="assignment"><br>

    <label for="grade">Grade</label>
    <input type="text" name="grade"><br>
    
    <input type="hidden" name="csrf_token" value="{}"> 

    <input type="submit" value="Submit">
</form>

<h2>Existing Grades</h2>
""".format(session['csrf_token']) #Added

#SHOWING
    
    for g in Grade.select():
        body += """
<div class="grade">
{}, {}: {}
</div>
""".format(g.student, g.assignment, g.grade)

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)

