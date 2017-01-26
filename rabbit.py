import urllib.request as req
import json
import re
import time
import sys

try:
    url = sys.argv[1] + ".json"
except:
    print("No URL given...")
    
count = 0
run = True
ceddit = 'https://api.pushshift.io/reddit/search?ids='
deleted = False

def exitLoop():
    global run
    global count
    run = False

    return "\nEnd of rabbit hole. Found " + str(count) + " nodes."

def findLink():
    global url
    global count
    global deleted
    deleted = False

    try:
        res = req.urlopen(req.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}))
        data = res.read()
        jres = json.loads(data.decode(res.info().get_content_charset("utf-8")))
        body = jres[1]["data"]["children"][0]["data"]["body"]
        commentId = jres[1]["data"]["children"][0]["data"]["id"]

        # if comment is removed, look it up on ceddit.com
        if (body == "[removed]"):
            try:
                res = req.urlopen(req.Request(ceddit + commentId, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}))
                data = res.read()
                jres = json.loads(data.decode(res.info().get_content_charset("utf-8")))
                body = jres["data"][0]["body"]
                timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(jres["data"][0]["created_utc"]))
                deleted = True
            except:
                return exitLoop()
        else:
            timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(jres[1]["data"]["children"][0]["data"]["created"]))

        link = "https://www." + body[body.find("reddit.com/r/"):[l.start() for l in re.finditer("/", body[body.find("reddit.com/r/"):])][5] + body.find("reddit.com/r/") + 8] + ".json"
    except:
        # if someone misplaced the 'roo, eg they linked the child of the 'roo
        try:
            parentId = jres[1]["data"]["children"][0]["data"]["parent_id"][3:]
            link = "https://www.reddit.com" + jres[0]["data"]["children"][0]["data"]["permalink"] + parentId + ".json"
        except:
            return exitLoop()
    
    count += 1
    url = link
    returnString = (str(count) + ". " + timestamp + " --- " + link).split(".json")[0]

    if (deleted):
        return returnString + " [node deleted]"
    else:
        return returnString

while(run):
    print(findLink())
