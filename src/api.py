import os, time,json

from requests.models import HTTPError, ReadTimeoutError, Response
from sodapy import Socrata
from utils import fileExists, loadJSONFile, log, logResults, saveFile, stripChars
from requests import ReadTimeout


socrata_domain = os.environ.get('socrata_domain')
socrata_dataset_identifier = os.environ.get('socrata_dataset_identifier')
appToken = os.environ.get('appToken')
socrata_token = os.environ.get('socrata_token')
socrata_timeout = int(os.environ.get('socrata_timeout'))
showExecutionTimes = os.environ.get('showExecutionTimes')


class APIResponse():
    def __init__(self) -> None:
        self.response = None
        self.error = None
        self.isOK = False
        self.fromCachedResponse = False
    
    def save(self, fileName=None):
        if fileName is None:
            raise 'fileName not provided!'
        saveFile(fileName, self.response)


class Api():
    def __init__(self):
        self.client = self.getConnection()

    def getConnection(self):
        log('Getting a connection to socrata')
        return Socrata(socrata_domain, socrata_token,timeout=socrata_timeout)


    def query(self, **kwargs):
        # log("Executing query: %s" % (json.dumps([kwargs])))
        if showExecutionTimes == 'True':
            start = time.time()
        global client
        res = APIResponse()

        cachedFile = None
        if ('query' in kwargs):
            queryName  = stripChars(kwargs.get('query'))
            cachedFile = 'results/%s.json' % queryName
        
        if fileExists(cachedFile):
            # log("using cached file")
            res.response = loadJSONFile(cachedFile)
            res.isOK = True
            res.fromCachedResponse = True
            return res
        else:
            try:
                data = self.client.get(socrata_dataset_identifier,**kwargs)
                res.response = data
                # log("Saving results")
                res.isOK = True
            except (ReadTimeout,ReadTimeoutError) as e:
                msg = "Timeout while fetching the data, either optimize the query, or try a higher timeout when connecting"
                log(msg, 'ERROR')
                res.error = msg
            except HTTPError as e:
                res.error = e
                log("HTTP Error! %s" % str(str(e).split(":")[0]))
            except Exception as e:
                res.error = e
                log("Unexpected Error! %s" % str(str(e).split(":")[0]))
            
            if showExecutionTimes == 'True':
                end = time.time()
                # log("API call done in %d seconds" % (round(end - start, 2)))
            if res.response is not None:
                res.save(cachedFile)
                return res
            else:
                return res









def getConnection():
    return Socrata(socrata_domain, socrata_token,timeout=socrata_timeout)


# def query(**kwargs):
#     log("Executing query: %s" % (json.dumps([kwargs])))
#     if showExecutionTimes == 'True':
#         start = time.time()
#     global client

#     res = APIResponse()
#     try:
#         res.response = client.get(,**kwargs)
#         log("Saving results")
#         logResults(json.dumps(kwargs), json.dumps(res.response))
#     except (ReadTimeout,ReadTimeoutError) as e:
#         msg = "Timeout while fetching the data, either optimize the query, or try a higher timeout when connecting"
#         log(msg, 'ERROR')
#         res.error = msg
#     except HTTPError as e:
#         res.error = e
#         log("HTTP Error! %s" % str(str(e).split(":")[0]))
#     except Exception as e:
#         res.error = e
#         log("Unexpected Error! %s" % str(str(e).split(":")[0]))
    
#     if showExecutionTimes == 'True':
#         end = time.time()
#         log("API call done in %d seconds" % (round(end - start, 2)))
#     return res

client = getConnection()