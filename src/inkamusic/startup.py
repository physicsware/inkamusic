# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2019  Udo Wollschläger

"""
# pylint: disable=locally-disabled, protected-access

import os
import random
import cherrypy

import inkamusic.const as const
import inkamusic.webutilities as webutilities

def start():

    package_dir = os.path.dirname(const.__file__)

    # initialize random numbers
    random.seed()

    # prepare cherrypy

    # KEY_DIR = 'inkamusic/keys/'  # location of ssl keys, if used
    # LOG_DIR = './logs/'  # location log files, if used
    
    CONF = {'/': {'tools.sessions.on': True, 'tools.staticdir.root': package_dir},
            '/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': const.STAT_DIR}
            }

    # remove # to activate logs
    # cherrypy.log.access_file = LOG_DIR + 'accesstest.txt'
    # cherrypy.log.error_file = LOG_DIR + 'errortest.txt'

    if const.HTTPS_PORT == 0:  # no https support

        cherrypy.server.socket_host = '::'  # '0.0.0.0'
        cherrypy.server.socket_port = const.HTTP_PORT
    else:

        SERVER = cherrypy._cpserver.Server()
        SERVER.socket_host = '::'  # "0.0.0.0"
        SERVER.socket_port = const.HTTP_PORT
        SERVER.subscribe()

        cherrypy.server.socket_host = '::'  # '0.0.0.0'
        cherrypy.server.socket_port = const.HTTPS_PORT
        cherrypy.server.ssl_module = 'builtin'
        cherrypy.server.ssl_private_key = KEY_DIR + const.HTTPS_KEY_FILE
        cherrypy.server.ssl_certificate = KEY_DIR + const.HTTPS_CERTIFICATE_FILE
        if const.HTTPS_INTERMEDIATE_FILE != '':
            cherrypy.server.ssl_certificate_chain = KEY_DIR + const.HTTPS_INTERMEDIATE_FILE

    cherrypy.quickstart(webutilities.InkaAlgorithmicMusicWebInterface(), '/', CONF)
