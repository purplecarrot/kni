import os
import platform
import sys
from flask import jsonify, request, url_for
from kni import app


@app.route('/')
@app.route('/v1/')
@app.route('/v1')
def index():
    """ return all available endpoints in this module """

    endpoints = {}

    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods:
            if rule.endpoint != 'static':
                endpoints[url_for(rule.endpoint)] = app.view_functions[rule.endpoint].__doc__
    
    app.logger.debug(endpoints)
    return endpoints


@app.route('/v1/headers', methods=['GET', 'POST'])
def http_headers():
    """ return HTTP headers sent """

    d = {k: v for k, v in request.headers.items()}
    app.logger.debug(d)
    return d


@app.route('/v1/knative', methods=['GET'])
def knative():
    """ return KNative OS environment variables """

    os_vars = ('HOSTNAME', 'K_SERVICE', 'K_REVISION', 
               'K_CONFIGURATION', 'TEST_MESSAGE')

    d = { var: os.getenv(var) for var in os_vars }
    app.logger.debug(d)
    return d


@app.route('/v1/env')
def env():
    """ return OS environment variables from inside container """

    d = {k: v for k, v in os.environ.items()}
    app.logger.debug("returned {} environment variables".format(len(d.keys())))
    return d


@app.route('/v1/post', methods=['GET', 'POST'])
def postdump():
    """ return dump of form or JSON data that was POSTed """

    r = { "mimetype": request.mimetype }

    if request.is_json:
        r['json'] = request.json
    else:
        r['form'] = { k: v for k, v in request.form.items() }
    app.logger.debug(r)
    return jsonify(r)


@app.route('/v1/cookies', methods=['GET', 'POST'])
def cookies():
    """ return cookies sent in """

    return request.cookies


@app.route('/v1/os', methods=['GET', 'POST'])
def osinfo():
    """ return information about underlying OS and Python interpreter """

    d = {}
    d['os'] = "{} {}".format(platform.system(), platform.release())
    d['python'] = '.'.join(platform.python_version_tuple())
    app.logger.debug()
    return d


@app.route('/healthz', methods=['GET'])
def healthz():
    """ Kubernetes healthcheck endpoint for liveness/readiness probes """

    return "ok\n"
