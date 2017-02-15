import httplib
import urllib
import ssl

def main_microsoft(args):

    prediction = {}

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': args.microsoft_key
    }

    # Request parameters
    params = urllib.urlencode({
        'language': 'unk',
        'detectOrientation': 'true',
    })

    if args.img_type == 'FILE':
        body = open(args.img_path, "rb")
        headers['Content-Type'] = 'application/octet-stream'

    else:
        body = '{\'URL\': \'' + args.img_path + '\'}'

    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com', context=gcontext)
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        prediction = response.read()
        conn.close()
    except Exception as e:
        print("Error: %s" % str(e))

    return prediction
