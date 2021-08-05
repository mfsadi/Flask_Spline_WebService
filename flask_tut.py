# -*- coding: utf-8 -*-
import os
import PIL
import urllib
import ast
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import CubicSpline
from flask import Flask, render_template, send_from_directory, request, current_app, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap= Bootstrap(app) # using Flask_Bootstrap to provide simple and efficient UI

class PhotoForm(FlaskForm): # Making Flask Form to revieve user data

    t = StringField('t (Provide a list representation such as [0, 0, 0, 0, 1, 1, 1, 1])', validators=[DataRequired()])
    c = StringField('c (Provide a list representation such as [[150, 160, 170, 190], [200, 140, 80, 30]], first comes x values, then y values)', validators=[DataRequired()])
    k = IntegerField('k (Provide a Scaler)', validators=[DataRequired()])
    photo = FileField('An image', validators=[FileRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index(): # View function for the Main Page 
    form = PhotoForm()
    if form.validate_on_submit(): # Getting input
        t = form.t.data
        c = form.c.data
        k = form.k.data

        form.t.data = ''
        form.c.data = ''
        form.k.data = ''

        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+'\\static\\photos\\' + filename)
        spline(filename, t, c, k) # Calling spline function below
        return render_template('index.html', form=form, t=t, c=c, k=k, image_name=filename)
    return render_template('index.html', form=form)	# Load page without doing anything


def spline(img_name, t, c, k):
    parameter_err=True
    t_list=[]
    k_list=[]
    try: # Checking whether to use default values
        t_list= ast.literal_eval(t) 
        k_list= ast.literal_eval(c)
        parameter_err=False

    except:
        parameter_err=True

    img = np.flipud(PIL.Image.open(app.root_path+'/static/photos/'+img_name))
    fig, ax = plt.subplots()
    plt.gca().invert_yaxis()
    ax.imshow(img) # Set image as the background to plot spline over it
    nodes = np.array( [[150, 200], [160, 150], [180, 60], [190, 30]] )
    x = nodes[:,0]
    y = nodes[:,1]
    tck,u = interpolate.splprep( [x,y] ,s = 0 )
    default_values=[[0, 0, 0, 0, 1, 1, 1, 1], [[150, 160, 170, 190], [200, 140, 80, 30]], 3]
	
    if parameter_err:
        xnew,ynew = interpolate.splev(np.linspace( 0, 1, 100 ), default_values,der = 0)

    else:
        xnew,ynew = interpolate.splev(np.linspace( 0, 1, 100 ), [[i for i in t_list], [j for j in k_list], k],der = 0)

    plt.plot( x,y,'o' , xnew ,ynew )
    plt.legend( [ 'data' , 'spline'] )
    plt.axis( [0, 300 , 0 , 400])
    fig.savefig(app.root_path+'/static/photos/'+'spline_'+img_name)


if __name__ == '__main__':
    app.run(debug=True)