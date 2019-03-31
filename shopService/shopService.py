import json
import sys
import BaseHTTPServer
import common
from BaseHTTPServer import BaseHTTPRequestHandler
import logging
import time

sidecarPort = 80
logger = logging.getLogger("root")


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v6/shop/items':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "items":
                    [{"itemId": "001", "itemName": "cloth"},
                          {"itemId": "002", "itemName": "cloth1"},
                          {"itemId": "003", "itemName": "cloth2"}
                          ]
                   }
            self.wfile.write(json.dumps(msg))
        elif "anynumber" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {"path": self.path}
            self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/shop/order':
            headers = common.build_trace_headers(self)
            headers['x-trace-service'] = "shop"
            if common.sendAndVerify("promotion", sidecarPort, "/api/v6/promotion/query", headers):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                msg = {
                    "userId": "1234",
                    "itemId": "002"
                }
                self.wfile.write(json.dumps(msg))
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                msg = {"exception":"Error invoke %s" % "/api/v6/promotion/query"}
                self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/product/deliver':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "itemId": "002",
                "destination": "shenzhen"
            }
            self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/sleep':
            time.sleep(5)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "items":
                    [{"itemId": "001", "itemName": "cloth"},
                     {"itemId": "002", "itemName": "cloth1"},
                     {"itemId": "003", "itemName": "cloth2"}
                     ]
            }
            self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/%7bparam%7d':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "items":
                    [{"itemId": "001", "itemName": "cloth"},
                     {"itemId": "002", "itemName": "cloth1"},
                     {"itemId": "003", "itemName": "cloth2"}
                     ]
            }
            self.wfile.write(json.dumps(msg))
        elif self.path == '/api/v6/{test}':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "items":
                    [{"itemId": "001", "itemName": "cloth"},
                     {"itemId": "002", "itemName": "cloth1"},
                     {"itemId": "003", "itemName": "cloth2"}
                     ]
            }
            self.wfile.write(json.dumps(msg))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "status":"UP"
            }
            self.wfile.write(json.dumps(msg))
        else:
            self.send_error(404, "{\"message\":\"File not found.\"}")
            return


if __name__ == '__main__':
    # Start a simple server, and loop forever
    ServerClass  = BaseHTTPServer.HTTPServer
    hostPort = int(sys.argv[1])
    # hostPort = 8091
    print "host port is %s"%hostPort
    logger.info("host port is %s"%hostPort)
    server = ServerClass(('0.0.0.0', hostPort), TodoHandler)
    print "Starting shopService, use <Ctrl-C> to stop"
    logger.info("Starting shopService, use <Ctrl-C> to stop")
    server.serve_forever()

