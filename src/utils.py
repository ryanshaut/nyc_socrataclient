import json
import time
import uuid
import datetime
import re
from os import path
import random

def prettyJson(data):
    if type(data) == type("string"):
        parsed = json.loads(data)
    if type(data) == type({}): # dict
        parsed = data
    else:
        parsed = data
    return (json.dumps(parsed, indent=4, sort_keys=True))

def log(msg=None, level=None):
    now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if level is None:
        level = "INFO"
    else:
        level = level.upper()
    message = "[%s] %s %s" % (now, level, msg)
    print(message)
    return message

def fileExists(fileName) -> bool:
    return path.exists(fileName)

def logResults(query, data):
    randomString = str(uuid.uuid4())[0:8]
    queryFile = "results/%s_query.json" % randomString
    dataFile = "results/%s_data.json" % randomString
    saveFile(queryFile, query)
    saveFile(dataFile, data)

def saveFile(file, data):
    with open(file, 'w') as outfile:
        outfile.writelines(json.dumps(data))

def loadFile(file):
    if fileExists(file):
        try:
            with open(file,'r') as infile:
                data = infile.readlines()
            return data
        except Exception as e:
            return None
    return None

def loadJSONFile(path):
    return json.load(open(path, 'r'))
    # with open(path,'r') as iFile:
    #     data = iFile.readlines()
    # return json.loads(data[0])

def stripChars(text) -> str:
    return re.sub('\W','',text)

# rounds to the nearest second
def timeDelta(start, end, fmt, output):
    s = datetime.datetime.strptime(start, fmt)
    e = datetime.datetime.strptime(end, fmt)
    deltaSeconds =  round((e - s).total_seconds())
    if output:
        if output.lower() == 'seconds':
            return deltaSeconds
        if output.lower() == 'minutes':
            return deltaSeconds / 60
        if output.lower() == 'hours':
            return deltaSeconds / 60 / 60
        if output.lower() == 'minutes':
            return deltaSeconds / 60 / 24
        raise "%s is not an output type!" % output
    else:
        return deltaSeconds


# input JSON list of objects
# returns an object of lists of those objects, including only what is specificed by attribs
# ex. input = [
# {x = 1, y = 11},
# {x = 2, y = 12},
# {x = 3, y = 13},
# ]
# returns
# {
#    x: [1,2,3],
#    y: [11,12,13]
# }
def extractFromJSON(data=None,attribs=None):
    if attribs is None:
        attribs = [k for k in data[0].keys()]
    #create the output structure
    output = {}
    for attrib in attribs:
        output[attrib] = []
    # loop over rows, then each key in the row and append the value to the proper list in output
    for row in data:
        for k in row.keys():
            if k in attribs:
                output[k].append(row[k])
    return output


def toDate(date,datefmt):
    return datetime.datetime.strptime(date, datefmt)

def getDOWFromDate(date, datefmt):
    try:
        return toDate(date, datefmt).strftime('%a')
    except Exception as e:
        return None


def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)