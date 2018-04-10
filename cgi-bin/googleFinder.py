#!/usr/bin/python
import urllib2
import cgi
import re
import json
print "Content-Type: text"
print "" #use this double quote print statement to add a blank line in the script

    
store = cgi.FieldStorage()
arrayJ = store.getvalue("array")
array = json.loads(arrayJ)
localita = ""
#array =["Informatica System","Easy Solution - Servizi Informatici","Simant Software Solutions","Sottokkio Gestionale di Fatturazione","S.I.O.Val. di Cuvato Damiano","Alchimie Mediali","Dataline S.r.l.","Ilovecomm S.r.l.","In.Va. Spa","Klinica S.n.c. di Gasperin Vladimiro & Melotti Leonardo","Logic Sistemi S.r.l.","Pastoret Engineering e Consulting S.r.l.","Plateroti Corrado","Pointer S.r.l.","Sintel Srl","Studio Saec S.n.c. di Sergio Enrico   C.","Studio Saec S.n.c. di Sergio Enrico & C.","Vallee Trafor S.r.l.","Youbit S.r.l.","C.D. Enterprise Srl"]
'''
is now possible to access the passed values by array[i]
'''
html = ""
url = "http://www.google.it/search?q="
config = '''+-bianche+-pagine+-gialle+-virgilio+-facebook+-wikipedia+-youtube+-linkedin+-yahoo+-twitter+-soldionline+-ditedi+-amazon+contatti'''+ localita
def parseResult(url):
    a = url.replace(" ","%20")
    return a
def regexLinks(html):
    res = []
    if html == "":
        return res
    m = re.findall('<h3.*?><a href="/url\?q=(.*?)".*?</h3>',html)
    for i in range(len(m)):       
        m[i] = re.sub("&amp(.*)","",m[i])
        res.append(m[i])
        if i == 0:  # modificando il parametro di confronto verranno restituiti piu link dalla ricerca 0 restituira un solo link
            break
    return res
results = []
for i in range(len(array)):
    pars = parseResult(array[i])
    urlGoogle = url + pars +config
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        html = opener.open(urlGoogle).read()
        link = regexLinks(html)
        for j in range(len(link)):  #TODO: gestire meglio la struttura dati nella quale sono posizionati i link, 3 per ogni pagina 
            results.append(link[j])
    except urllib2.HTTPError as e:
        continue
data={}
data["response"] = results
json_data = json.dumps(data)	
print(json_data)
#Attenzione Google blocchera' dopo un po la ricerca, impedendo di andare avanti
