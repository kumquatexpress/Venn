from flask import render_template
import models

def index():
	return render_template('index.html')