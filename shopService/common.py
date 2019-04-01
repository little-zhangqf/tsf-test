import sys
import httplib
import traceback

traceHeaders = ['x-request-id',
                'x-trace-service',
                'x-ot-span-context',
                'x-client-trace-id',
                'x-envoy-force-trace',
                'x-b3-traceid',
                'x-b3-spanid',
                'x-b3-parentspanid',
                'x-b3-sampled',
                'x-b3-flags',
                'testtag1',
                'test-tag2',
                'test_tag3',
                'TEST_TAG']

def sendAndVerify(ip, port, uri, headers):
    print >> sys.stderr, "start to invoke %s" % uri
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection(ip, port, timeout=30)
        headers["Content-type"] = "application/x-www-form-urlencoded"
        headers["Accept"] = "text/plain"
        httpClient.request("GET", uri, None, headers)
        response = httpClient.getresponse()
        retStatus = response.status
        if retStatus != 200:
            print >> sys.stderr, "Test fail, status code is %s\n" % retStatus
            return bool()
        data = response.read()
        print >> sys.stderr, "response data is %s\n" % data
        return bool(1)
    except Exception, e:
        print >> sys.stderr, "Test fail, status exception is %s" % e
        traceback.print_exc()
        return bool()
    finally:
        if httpClient:
            httpClient.close()

def build_trace_headers(handler):
    retHeaders = {}
    for header in traceHeaders:
        if handler.headers.has_key(header):
            header_value = handler.headers.get(header)
            retHeaders[header] = header_value
    return retHeaders

