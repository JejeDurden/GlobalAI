##------------------------------------------------------------##
#Imports
from app import app
from flask import make_response, render_template,send_from_directory,\
                    abort, jsonify, Blueprint, Flask, request,current_app

import os
import pandas as pd
import numpy as np
import json
from datetime import timedelta
from functools import update_wrapper

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##------------------------------------------------------------##
#set env
main = Blueprint('main', __name__)
#read csv
sku_df = pd.read_csv('data/sku_info/data.csv',encoding='utf-8',index_col=0)
#list files/images
files_list = os.listdir('data/sku_images/download')
#filter dataframe
sku_df = sku_df[sku_df['sku_code'].isin([x.strip(".jpg") for x in files_list])]
sku_df.drop_duplicates(['sku_code'],inplace=True)

#var
material_list = list(set(sku_df.aesthetic_sub_line))
material_list = sorted([str(x) for x in material_list])
colour_list = list(set(sku_df.color))
colour_list = sorted([str(x) for x in colour_list])
category_list = list(set(sku_df.function))
category_list = sorted([str(x) for x in category_list])


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
##------------------------------------------------------------##

sim = np.fromfile('data/saved_model/distance_matrix_complete.dat', dtype=float)
sim = sim.reshape((len(files_list), len(files_list)))

def get_similar(sim, idx, N=10):
    row = sim[idx, :]
    out = []
    coef = []
    for x in np.argsort(-row)[:N]:
        out.append(files_list[x])
        coef.append(sim[idx, x])
    return out,coef

#compute
def compute(sim,sku_history,N=100):
    index_history =[files_list.index(x+".jpg") for x in sku_history]
    temp_df= pd.DataFrame()
    a_l,b_l=[],[]
    for element in index_history:
        a,b = get_similar(sim,element,N)
        a_l=a_l+a
        b_l=b_l+b
    temp_df['reco'] = a_l
    temp_df['score']= b_l

    #remove already seen items:
    temp_df = temp_df[~temp_df['reco'].isin([x+'.jpg' for x in sku_history])]
    temp_df = temp_df.groupby('reco').mean().sort_values('score',ascending=False)
    return temp_df

def recommend(sku_,param=None):
    sku_=sku_.split(",")
    output=compute(sim,sku_,14027).reset_index()
    output= list(output.reco)
    output = [x.strip(".jpg") for x in output]
    if param:
        a=sku_df.set_index("sku_code").reindex(output)
        a=a.reset_index()
        out=list(a[a["function"]==param]['sku_code'])
        #out = [x for x in output if x in out]
        return(json.dumps({"sku_list":out[0:50]}))
    else:
        return(json.dumps({"sku_list":output[0:50]}))
    #return(str(output))



##------------------------------------------------------------##
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/gallery.html/<color>')
def get_gallery(color):
    if color:
        image_names = list(sku_df[sku_df["color"]==color]["sku_code"])
        #rand=np.random.choice(range(0,len(image_names)),150)
        #image_names = [image_names[x] for x in rand]
        #image_names = [x.strip(".jpg") for x in image_names]
        return render_template("gallery.html", image_names=image_names,
                             colour_list = colour_list, material_list=material_list,
                              category_list=category_list)
    
@app.route('/gallery.html/')
def display():
    rand=np.random.choice(range(0,len(files_list)),150)
    image_names = [files_list[x] for x in rand]
    image_names = [x.strip(".jpg") for x in image_names]
    return render_template("gallery.html", image_names=image_names,
                             colour_list = colour_list, material_list=material_list,
                              category_list=category_list)

@app.route("/<sku>")
def reco(sku):
    sku=sku.split(",")
    output=compute(sim,sku,150).reset_index()
    output= list(output.reco)
    output = [x.strip(".jpg") for x in output]
    #return(json.dumps(output))
    return(str(output))



@app.route("/api/get", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def get_reco():
    if 'sku_history' in request.args:
        if request.args['sku_history']:
            return recommend(request.args['sku_history'],request.args["param"])
        else:
            return(json.dumps({"sku_list":[]}))
    if 'context' in request.args:
        rand=np.random.choice(range(0,len(files_list)),150)
        image_names = [files_list[x] for x in rand]
        image_names = [x.strip(".jpg") for x in image_names]
        return (json.dumps({"sku_list":image_names[0:75],"material_list":material_list,"colour_list":colour_list,"category_list":category_list}))
    else:
        return "WHAAAAAAAAAAT?"



@app.route("/api/filter", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def filter_catalog():
    df = sku_df
    if "colour" in request.args:
        colour=request.args['colour']
        if colour:
            df=df[df["color"]==colour]
    else:
        color=None
    if "material" in request.args:
        material = request.args['material']
        if material:
            df = df[df["aesthetic_sub_line"]==material]
    else:
        material=None
    if "category" in request.args:
        category = request.args['category']
        if category:
            df = df[df["function"]==category]
    else:
        category = None
    image_names = list(df["sku_code"])
    #rand=np.random.choice(range(0,len(image_names)),150)
    #image_names = [image_names[x] for x in rand]
    if len(image_names)>75:
        rand=np.random.choice(range(0,len(image_names)),75)
        image_names = [image_names[x] for x in rand]
    else:
        image_names=image_names[0:75]
    return(json.dumps({"sku_list":image_names}))
    