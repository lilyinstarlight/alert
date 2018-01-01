import fooster.web, fooster.web.form, fooster.web.page

from alert import config, alert


http = None

routes = {}
error_routes = {}


class Interface(fooster.web.page.PageHandler, fooster.web.form.FormHandler):
    directory = config.template
    page = 'index.html'
    message = ''

    def format(self, page):
        return page.format(message=self.message)

    def do_post(self):
        try:
            body = self.request.body['body']
        except (KeyError, TypeError):
            raise fooster.web.HTTPError(400)

        try:
            alert.send(body)

            self.message = 'Successfully sent alert.'
        except:
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
