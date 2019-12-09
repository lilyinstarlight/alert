import argparse
import importlib.util
import logging
import signal
import sys

import fooster.web

from alert import config


def main():
    parser = argparse.ArgumentParser(description='serve up an alert service')
    parser.add_argument('-a', '--address', dest='address', help='address to bind')
    parser.add_argument('-p', '--port', type=int, dest='port', help='port to bind')
    parser.add_argument('-t', '--template', dest='template', help='template directory to use')
    parser.add_argument('-l', '--log', dest='log', help='log directory to use')
    parser.add_argument('auth', help='auth file to use')

    args = parser.parse_args()

    if args.address:
        config.addr = (args.address, config.addr[1])

    if args.port:
        config.addr = (config.addr[0], args.port)

    if args.template:
        config.template = args.template

    if args.log:
        if args.log == 'none':
            config.log = None
            config.http_log = None
        else:
            config.log = args.log + '/alert.log'
            config.http_log = args.log + '/http.log'

    auth_spec = importlib.util.spec_from_file_location('auth', args.auth)
    auth = importlib.util.module_from_spec(auth_spec)
    auth_spec.loader.exec_module(auth)

    config.source = auth.source
    config.number = auth.number
    config.auth = auth.auth


    # setup logging
    log = logging.getLogger('alert')
    log.setLevel(logging.INFO)
    if config.log:
        log.addHandler(logging.FileHandler(config.log))
    else:
        log.addHandler(logging.StreamHandler(sys.stdout))

    if config.http_log:
        http_log_handler = logging.FileHandler(config.http_log)
        http_log_handler.setFormatter(fooster.web.HTTPLogFormatter())

        logging.getLogger('http').addHandler(http_log_handler)


    from alert import name, version
    from alert import http


    log.info(name + ' ' + version + ' starting...')

    # start everything
    http.start()


    # cleanup function
    def exit(signum, frame):
        http.stop()


    # use the function for both SIGINT and SIGTERM
    for sig in signal.SIGINT, signal.SIGTERM:
        signal.signal(sig, exit)

    # join against the HTTP server
    http.join()


if __name__ == '__main__':
    main()
