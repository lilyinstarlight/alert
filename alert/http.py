import logging

import fooster.web
import fooster.web.form
import fooster.web.page

from alert import config, alert


http = None

routes = {}
error_routes = {}


log = logging.getLogger('alert')


class Interface(fooster.web.form.FormMixIn, fooster.web.page.PageHandler):
    directory = config.template
    page = 'index.html'
    message = ''

    def format(self, page):
        return page.format(message=self.message)

    def do_post(self):
        try:
            body = ('Alert: ' + self.request.body['body']).strip()
        except (KeyError, TypeError):
            raise fooster.web.HTTPError(400)

        try:
            alert.send(body)

            self.message = 'Successfully sent alert.'
        except Exception:
            log.exception('Caught exception while trying to send alert')

            self.message = 'Failed to send alert.'

        return self.do_get()


class ErrorInterface(fooster.web.page.PageErrorHandler):
    directory = config.template
    page = 'error.html'


routes.update({'/': Interface})
error_routes.update(fooster.web.page.new_error(handler=ErrorInterface))


def start():
    global http

    http = fooster.web.HTTPServer(config.addr, routes, error_routes)
    http.start()


def stop():
    global http

    http.stop()
    http = None


def join():
    global http

    http.join()
