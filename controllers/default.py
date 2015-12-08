# -*- coding: utf-8 -*-

from gluon.custom_import import track_changes; 
track_changes(True)


def index():
    return dict()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def what():
    import urllib
    try:
        images = XML(urllib.urlopen(
            'http://www.web2py.com/poweredby/default/images').read())
    except:
        images = []
    return response.render(images=images)


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def download():
    return response.render()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def who():
    return response.render()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def support():
    return response.render()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def documentation():
    return response.render()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def usergroups():
    return response.render()


def contact():
    redirect(URL('default', 'usergroups'))


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def videos():
    return response.render()


def security():
    redirect('http://www.web2py.com/book/default/chapter/01#Security')


def api():
    redirect('http://www.web2py.com/book/default/chapter/04#API')


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def license():
    import os
    filename = os.path.join(request.env.gluon_parent, 'LICENSE')
    return response.render(dict(license=MARKMIN(read_file(filename))))

def version():
    if request.args(0)=='raw':
        return request.env.web2py_version
    from gluon.fileutils import parse_version
    (a, b, c, pre_release, build) = parse_version(request.env.web2py_version)
    return 'Version %i.%i.%i (%.4i-%.2i-%.2i %.2i:%.2i:%.2i) %s' % (
        a,b,c,build.year,build.month,build.day,
        build.hour,build.minute,build.second,pre_release)

@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def examples():
    return response.render()


@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def changelog():
    import os
    filename = os.path.join(request.env.gluon_parent, 'CHANGELOG')
    return response.render(dict(changelog=MARKMIN(read_file(filename))))
