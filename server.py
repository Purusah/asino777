import tornado.ioloop
import tornado.web
from jsonrpcserver.aio import methods
import method
from jsonrpcserver.response import NotificationResponse
#import casino

port = 8001
host = f"http://localhost:{port}"



class MainHandler(tornado.web.RequestHandler):
    async def post(self):
        request = self.request.body.decode()
        response = await methods.dispatch(request)
        if not response.is_notification:
            self.write(str(response))


def make_app():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    return application


if __name__ == '__main__':
    app = make_app()
    app.listen(8001)
    tornado.ioloop.IOLoop.current().start()