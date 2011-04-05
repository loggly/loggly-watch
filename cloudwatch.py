import os
import httplib2, base64, hashlib, hmac, time
from urllib import urlencode, quote_plus

def getSignedURL(key, secret_key, action, parms):

    # base url
    base_url = "monitoring.amazonaws.com"

    # build the parameter dictionary
    url_params = parms
    url_params['AWSAccessKeyId'] = key
    url_params['Action'] = action
    url_params['SignatureMethod'] = 'HmacSHA256'
    url_params['SignatureVersion'] = '2'
    url_params['Version'] = '2010-08-01'
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    # sort and encode the parameters
    keys = url_params.keys()
    keys.sort()
    values = map(url_params.get, keys)
    url_string = urlencode(zip(keys,values))

    # sign, encode and quote the entire request string
    string_to_sign = "GET\n%s\n/\n%s" % (base_url, url_string)
    signature = hmac.new( key=secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest()
    signature = base64.encodestring(signature).strip()
    urlencoded_signature = quote_plus(signature)
    url_string += "&Signature=%s" % urlencoded_signature

    # do it
    foo = "http://%s/?%s" % (base_url, url_string)
    return foo

class connection:
    def __init__(self, key, secret_key):
        self.key = os.getenv('AWS_ACCESS_KEY_ID', key)
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY_ID', secret_key)

    def putData(self, namespace='Loggly', metricname='EventCount', value=0):
        foo = getSignedURL(self.key, self.secret_key, 'PutMetricData', {'Namespace': namespace, 'MetricData.member.1.MetricName': metricname, 'MetricData.member.1.Value': value})
        h = httplib2.Http()
        resp, content = h.request(foo)
