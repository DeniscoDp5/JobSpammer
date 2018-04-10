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
#array =["http://www.e-laser.it/wordpress/%3Fpage_id%3D167","https://www.paginegialle.it/quart-ao/informatica/nuova-vallelabor-g.-cheillon-c.","http://www.siam-srl.it/contatti_3.html","http://016661088.telefono.click/016661088-ricossa-alessandro-aosta.html","http://www.infosys.it/la-storia/contatti/","http://www.easycare.solutions/","http://www.simant.it/","http://www.sioval.com/contatti.html","https://www.alchimiemediali.it/RW/","https://it.kompass.com/c/american-dataline-srl/it0110425/","https://www.ilovecomm.com/","http://www.invallee.it/inva/index.php/ita/pagina/50/","https://www.paginegialle.it/aosta-ao/informatica/klinica-gasperin-v.-melotti-l.","https://www.aimsafe.it/static/about.php","http://www.pastoret.it/","http://016540740.telefono.click/","http://www.pointersrl.it/","http://www.sintel.net/","https://www.saec.net/","https://www.saec.net/","http://www.valleetrafor.it/","https://www.youbit.it/","http://www.cd-enterprise.it/contatti.html"]
results = []
regex = ''' (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]) '''
regex2 = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
text_probe = """ <strong>denisco.dp5@gmail.com probe.iy<strong> <p>gmail.com@hei.it.hole</p> """

def regexEmail(input):
    res = []
    if input == "":
        return res
    m = re.findall(regex2,input)
    for i in range(len(m)):
        boole = True       
        for j in range(len(res)):
            if m[i] == res[j]:
                boole = False
        if boole == True:
            res.append(m[i])
            #print(m[i])
    return res

for i in range(len(array)):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        html = opener.open(array[i]).read()
        #print(i)
        #print(html)
        emailArray = regexEmail(html)
        for j in range(len(emailArray)):  #TODO: gestire meglio la struttura dati nella quale sono posizionati i link, 3 per ogni pagina 
            results.append(emailArray[j])
    except (urllib2.HTTPError, urllib2.HTTPDefaultErrorHandler, urllib2.URLError) as e:
        continue
data={}
data["response"] = results
json_data = json.dumps(data)	
print(json_data)