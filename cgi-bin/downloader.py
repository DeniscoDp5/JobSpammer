#!/usr/bin/python
import urllib2
import cgi
import re
import json
print "Content-Type: text"
print "" #use this double quote print statement to add a blank line in the script

    
store = cgi.FieldStorage()
category = store["category"].value
location = store["location"].value

def parseResponse( htmlResponse):
		htmlResponse = htmlResponse.replace('\n',"")
		htmlResponse = htmlResponse.replace('\t',"")
		htmlResponse = htmlResponse.replace('\r',"")
 		divSelect = str('<h1 itemprop="name" class="fn elementTitle"><a')
		m = re.findall(divSelect+'(.*?)</h1>',htmlResponse)
		for i in range(len(m)):
			aux = re.findall('">(.*?)</a>',str(m[i]))
			m[i] = aux[0]
		return m	

def parseResponse2( parsedI ):
	for i in range(len(parsedI)):
		aux = re.findall('<strong>(.*?)</strong>',parsedI[i])
		if len(aux) > 0:
			line = re.sub("<strong>(.*)</strong>",aux[0],parsedI[i])
			parsedI[i] = line
	return parsedI

urlI = "http://www.paginegialle.it/ricerca/" + category +"/"+ location +"/p-"
urlII ="?mr=50"
html = ""

try:
    i = 1
    while True:
        url = urlI + str(i) + urlII
        #print(url)
        response=urllib2.urlopen(url)
        html = html + response.read()
        i=i+1
except  urllib2.HTTPError:
	out = parseResponse(html)
	out2 = parseResponse2(out)
	data={}
	data["response"] = out2
	json_data = json.dumps(data)
	print(json_data)

