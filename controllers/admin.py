# -*- coding: utf-8 -*-

from gluon.custom_import import track_changes; 
track_changes(True)

def index():
    redirect(URL(c='default', f='user'))
