import json
import time
import uuid

def prettyJson(data):
    if type(data) == type("string"):
        parsed = json.loads(data)
    if type(data) == type({}): # dict
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

def logResults(query, data):
    randomString = str(uuid.uuid4())[0:8]
    queryFile = "results/%s_query.json" % randomString
    dataFile = "results/%s_data.json" % randomString
    with open(queryFile, 'w') as outfile:
        outfile.writelines(prettyJson(query))
    with open(dataFile, 'w') as outfile:
        outfile.writelines(prettyJson(data))

def loadJSONFile(path):
    return json.load(open(path, 'r'))
    # with open(path,'r') as iFile:
    #     data = iFile.readlines()
    # return json.loads(data[0])


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
