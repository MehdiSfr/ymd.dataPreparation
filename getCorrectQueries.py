__author__ = 'Mehdis'

import threading
import requests
import json

linePerThreas = 10


def worker(num):
    """thread worker function"""
    fr = open('/Users/Mehdis/Documents/programs/yourmd/languageModel/querylog_filtered_100.txt', 'r')
    correctLines = []
    lineCounter = 1
    jsQuery = {}
    headers = {'content-type': 'application/json'}
    for line in fr.readlines():
        if (lineCounter > num * linePerThreas and lineCounter < (num + 1) * linePerThreas):
            jsQuery["message"] = line.strip()
            response = requests.post('http://zuul.dev.your.md/spell-checker/check', data=json.dumps(jsQuery),
                                     headers=headers)
            jsonOutput = eval(response.text)
            if jsonOutput["correctedMessage"] == line.strip():
                correctLines.append(line)
        lineCounter += 1
    fr.close()

    with open('/Users/Mehdis/Documents/programs/yourmd/languageModel/maps/ql_' + str(num) + '.txt', 'w') as fw:
        for item in correctLines:
            fw.write(item)
    print('Worker: %s done!' % num)
    return


threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
