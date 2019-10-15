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

import const
import webutilities

def error_page_404(status, message, traceback, version):
    """error page for http error 404"""
    del traceback  # pylint warning
    html = "Error {}. {}. {} - Well, I'm very sorry but you haven't paid!".format(status, message, version)
    html += """<a href ="/">back</a>"""
    return html


#if __name__ == '__main__':
def main():

    # initialize random numbers
    random.seed()

    # prepare cherrypy

    STAT_DIR = './public'  # static content
    KEY_DIR = './keys/'  # location of ssl keys, if used
    LOG_DIR = './logs/'  # log files
    print(os.path.abspath(os.getcwd()))
    CONF = {'/': {'tools.sessions.on': True, 'tools.staticdir.root': const.APP_DIR},
            '/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': STAT_DIR}
            }

    # cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.log.access_file = LOG_DIR + 'accesstest.txt'
    cherrypy.log.error_file = LOG_DIR + 'errortest.txt'

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


main()
