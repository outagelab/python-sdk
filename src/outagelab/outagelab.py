"""Main module."""

import http.client

outagelab_host = "app.outagelab.com"

def getresponse(self, *k, **kw):
    res = _getresponse(self, *k, **kw)

    try:
        if outagelab_host in res.url:
            return res
    except:
        pass
    finally:
        return res


_getresponse = http.client.HTTPConnection.getresponse
http.client.HTTPConnection.getresponse = getresponse
