import urllib.request as req
import json
import re
import time
import sys

try:
	url = sys.argv[1]
	try:
		url = contents[:[l.start() for l in re.finditer("/", contents)][8]] + ".json"
	except IndexError:
		url = contents[:contents.find("?context")] + ".json"
except:
    # random comment that starts the rabbit hole that I found
    url = "https://www.reddit.com/r/gaming/comments/5o72wo/oh_shi_oh_my_goooood/dchl7nn.json"
count = 0
run = True

def exitLoop():
    global run
    global count
    run = False

    return "\nEnd of rabbit hole. Found " + str(count) + " nodes."

def findLink():
    global url
    global count

    try:
        res = req.urlopen(req.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}))
        data = res.read()
        jres = json.loads(data.decode(res.info().get_content_charset("utf-8")))
        body = jres[1]["data"]["children"][0]["data"]["body"]
        
        if (body == "[removed]"):
            return exitLoop()
        
        timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(jres[1]["data"]["children"][0]["data"]["created"]))
        contents = body[body.find("(") + 1:body.find(")")]
    except:
        return exitLoop()
    
    try:
        link = contents[:[l.start() for l in re.finditer("/", contents)][8]] + ".json"
    except IndexError:
        link = contents[:contents.find("?context")] + ".json"

    count += 1
    url = link

    return str(count) + ". " + timestamp + " --- " + link

while(run):
    print(findLink())
