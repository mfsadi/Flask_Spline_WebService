# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, current_app, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import CubicSpline
import PIL
import urllib
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap= Bootstrap(app)

class PhotoForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        print(name)
        form.name.data = ''
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save('photos/' + filename)
        return render_template('index.html', form=form, name=name)
    return render_template('index.html', form=form, name=name)	

if __name__ == '__main__':
    app.run(debug=True)