##
## common function filter is used for all db to ensure privacy
##

import datetime
import os
from gluon import current
from gluon import *
import random

# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate

## to re-arrange the order of fields, you need to define your own table
#  as per Massimo: https://groups.google.com/forum/#!msg/web2py/M8vXPX6rExU/mI7oy8_WdCQJ
auth = Auth(db)
#auth.settings.extra_fields['auth_user']= [
  #Field('Company', 'string', requires=IS_NOT_EMPTY()),
  #Field('Phone')
#]
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy

### allow people to register and automatically log them in after registration 
# but still want to send an email for verification so that they cannot login 
# again after logout, unless they completed the instructions in the email : True
auth.settings.registration_requires_verification = False
auth.settings.login_after_registration = False
###
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')


#*************************************************************************************
# auth.user is used to restrict user access to db elements (projects of other users)
# using common_filter = lambda query: db.project.created_by == auth.user_id
#*************************************************************************************
	                
db.define_table('testimonial',
				db.Field('company_name', 'text', required=True),
				db.Field('text_', 'text', required=True),
				db.Field('date_', 'datetime', required=True, default=datetime.datetime.today()),
                
				db.Field('created_by', 'integer', default=auth.user_id, readable=False, writable=False),
                common_filter = lambda query: db.testimonial.created_by == auth.user_id,
                )
