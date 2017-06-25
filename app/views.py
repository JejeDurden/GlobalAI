#!/usr/bin/env python
# -*- coding: utf-8 -*-



##------------------------------------------------------------##
#Imports
from app import app,image_analyser as ia
from app import text_analysis as ta

from flask import make_response, render_template,send_from_directory,\
                    abort, jsonify, Blueprint, Flask, request,current_app
import os
import pandas as pd
import json
from datetime import timedelta
from functools import update_wrapper

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



##------------------------------------------------------------##
#set env
main = Blueprint('main', __name__)


#var
keys=['similar_images', 'titles', 'descriptions', 'links',"first_images_in_page"]
keys2=['title','bias',
 'bs',
 'conspiracy',
 'fake',
 'hate',
 'junksci',
 'mixture of true and false',
 'mostly false',
 'mostly true',
 'no factual content',
 'satire',
 'state']

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

def reverse_search(url):
    junk = ia.doImageSearch(url)
    out = ia.parseResults(junk)
    return out


##------------------------------------------------------------##
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"



@app.route("/api/get", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def get_image_info():
    if 'url_input_img' in request.args:
        if request.args['url_input_img']:
            return json.dumps(reverse_search(request.args["url_input_img"]))
        else:
            return(json.dumps({key: None for key in keys}))
    if 'url_input_page' in request.args:
        if request.args['url_input_page']:
            url = request.args["url_input_page"]
            links = ia.find_all_img(url)
            links = ia.get_biggest_imgs(links)
            out = reverse_search(links[0])
            out["first_images_in_page"]=links
            return json.dumps(out)
        else:
            return(json.dumps({key: None for key in keys}))
    if 'url_input_page2' in request.args:
        if request.args['url_input_page2']:
            url = request.args["url_input_page2"]
            text=ta.find_title(url)
            out=ta.pred_proba(text)
            out["title"]=text #ligne à modfier pour lui faire prendre le titre
            return json.dumps(out)
        else:
            return(json.dumps({key: None for key in keys2}))  
     
        
    else:
        return "WHAAAAAAAAAAT?"



