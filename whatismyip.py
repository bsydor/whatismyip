'''What Is My IP - Return client IP as plain text or json'''

import tornado.ioloop
import tornado.web
import logging, logging.handlers


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        '''GET handler'''
        syslog_handler = logging.handlers.SysLogHandler(address = '/dev/log', facility = logging.handlers.SysLogHandler.LOG_LOCAL0)
        log_format = logging.Formatter('whatismyip[%(process)d]: %(levelname)s %(message)s')
        syslog_handler.setFormatter(log_format)

        logger = logging.getLogger()
        logger.addHandler(syslog_handler)
        logger.setLevel(logging.INFO)

        #self.write("Hello, world")
        #logging.info('Got request from: %s' % repr(self.request.headers['X-Forwarded-For']))
        if 'X-Forwarded-For' in self.request.headers:
            client_ip = self.request.headers['X-Forwarded-For']
        else:
            client_ip = self.request.remote_ip

        if self.request.uri == '/all':
            self.write(repr(self.request))
        elif self.request.uri == '/json':
            self.write('{' + '"ip": ' + '"' + client_ip + '"}' + "\n")
        else:
            self.write(client_ip + "\n")

application = tornado.web.Application([
    (r"/.*", MainHandler),
])

if __name__ == "__main__":
    #application.listen(8888, address='127.0.0.1')
    application.listen(8888, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
