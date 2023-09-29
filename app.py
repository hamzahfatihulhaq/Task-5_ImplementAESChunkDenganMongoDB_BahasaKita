import tornado.web
import tornado.ioloop
from tornado.web import HTTPError
from Handlers.uploadHandler import UploadHandler
from Handlers.downloadHandler import DownloadHandler
from Handlers.htmlHandler import HTMLHandler
from Handlers.socketHanlder import ProgressWebSocket


def make_app():
    return tornado.web.Application([
        (r"/", HTMLHandler),
        (r"/upload", UploadHandler),
        (r"/download/(.*)", DownloadHandler),
        (r"/websocket", ProgressWebSocket)
    ],
    debug=True,
    autoreload=True
    )
def stop_server():
    tornado.ioloop.IOLoop.current().stop()

if __name__ == '__main__':
    progress_ws = None

    app = make_app()
    port = 8888

    server = tornado.httpserver.HTTPServer(app, max_buffer_size=10485760000, max_body_size=10485760000)
    server.listen(port)
    # app.listen(port)
    print(f'Server is listening on localhost on port {port}')
    
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        stop_server()
    except HTTPError as e:
        print(f"HTTP Error: {e.status_code} - {e.reason}")