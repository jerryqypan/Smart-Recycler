import httplib, urllib, base64
import re
def visionAPILink(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '14ac89f222ca4b3fa9158588fe6a7911',
    }

    params = urllib.urlencode({
        # Request parameters
        'visualFeatures': 'Categories,Tags,Description,Faces,ImageType,Color',
        'language': 'en',
    })
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, '{"url":"'+url+'"}', headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print url
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data
keywords=["bottle","can","drink_","beverage","drink_can","glass","newspaper","paper","book","envelope","card"]

JSON=visionAPILink("http://c3.staticflickr.com/4/3144/2859981714_c82940b8b8.jpg")
result = re.findall('"name":"(.*?)","', JSON)
tagsresult = re.findall('{"tags":(.*?)],',JSON)
tagsresult = re.findall(''"(.*?)"'',tagsresult[0])
print JSON
for item in result:
    if any(item in s for s in keywords):
        print "TRUE"
        break
for item in tagsresult:
    if any(item in s for s in keywords):
        print "LMAO"
        break

#print isinstance(JSON,basestring)