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

    CONF = {'/': {'tools.sessions.on': True, 'tools.staticdir.root': package_dir},
            '/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': const.STAT_DIR}
            }
    cherrypy.log.screen = False
    # cherrypy.log.error_file = package_dir + "/" + const.LOG_DIR + 'cherrypy_errlog.txt'
    # cherrypy.log.access_file = package_dir + "/" + const.LOG_DIR + 'cherrypy_access.txt'

    if const.HTTPS_PORT == 0:  # no https support

        cherrypy.server.socket_host = '::'  # '0.0.0.0'
        cherrypy.server.socket_port = const.HTTP_PORT
    else:

        SERVER = cherrypy._cpserver.Server()
        SERVER.socket_host = '::'  # "0.0.0.0"
        SERVER.socket_port = const.HTTP_PORT
        SERVER.subscribe()
        KEY_DIR = 'inkamusic/keys/'  # location of ssl keys, if used
        cherrypy.server.socket_host = '::'  # '0.0.0.0'
        cherrypy.server.socket_port = const.HTTPS_PORT
        cherrypy.server.ssl_module = 'builtin'
        cherrypy.server.ssl_private_key = KEY_DIR + const.HTTPS_KEY_FILE
        cherrypy.server.ssl_certificate = KEY_DIR + const.HTTPS_CERTIFICATE_FILE
        if const.HTTPS_INTERMEDIATE_FILE != '':
            cherrypy.server.ssl_certificate_chain = KEY_DIR + const.HTTPS_INTERMEDIATE_FILE

    print('')
    print('inkamusic is now running.')
    print('')
    print('Open a browser window and enter or copy this URL')
    print('')
    print('    http://127.0.0.1:8080')
    print(' ')
    print('to access the local web user interface.')
    print(' ')

    cherrypy.quickstart(webutilities.InkaAlgorithmicMusicWebInterface(), '/', CONF)
