from argparse import ArgumentParser
from base64 import b64decode
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRequestHandler

class XMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, host, port, username, password, *args, **kwargs):
        self.username = username
        self.password = password
        class RequestHandler(SimpleXMLRequestHandler):
            def parse_request(request):
                if SimpleXMLRequestHandler:
                    parse_request(request)
                    if self.authenticate(request.headers):
                        return True
                    else:
                        request.send_error(401, 'Authentication Failed')
                return False
        SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=RequestHandler, *args, **kwargs)
    def authenticate(self, headers):
        headers = headers.get("Authorization").split()
        basic, encoded = headers[0], headers[1]
        if basic != 'Basic':
            print("Only basic aunthentication supported")
            return False
        secret = b64decode(encoded).split(b':')
        username, password = secret[0].decode('utf-8'), secret[1].decode("utf-8")
        return True if (username == self.username and password == self.password) else False
def run_server(host, port, username, password):
    server = XMLRPCServer(host, port, username, password)
    def echo(msg):
        reply = msg.upper()
        print("Client:  ", reply)
    server.register_function(echo, 'I Love Programming So Much!')
    print("Running an HTTP auth enabled XMLRPC Server on [%s : %s] " % (host, port))
    server.serve_forever()
if __name__ == "__main__":
    parser = ArgumentParser(description="Multithreaded Multicall XMLRPC Server/Proxy")
    parser.add_argument('--host',, action='store', dest='host', default='127.0.0.1')
    parser.add_argument('--port',, action='store', dest='port', default=8000, type=int)
    parser.add_argument('--username',, action='store', dest='username', default='GhettoCole')
    parser.add_argument('--password',, action='store', dest='password', default='ComputerGeeks')
    args = parser.parse_args()
    host, port = args.host, args.port
    username, password = args.username, args.password
    run_server(host, port, username, password)