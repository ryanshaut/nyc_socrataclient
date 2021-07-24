import os, time, uuid,json

from requests.models import HTTPError, ReadTimeoutError
from sodapy import Socrata
from utils import log, logResults
from requests import ReadTimeout


socrata_domain = os.environ.get('socrata_domain')
socrata_dataset_identifier = os.environ.get('socrata_dataset_identifier')
appToken = os.environ.get('appToken')
socrata_token = os.environ.get('socrata_token')
socrata_timeout = int(os.environ.get('socrata_timeout'))
showExecutionTimes = os.environ.get('showExecutionTimes')



def getConnection():
    return Socrata(socrata_domain, socrata_token,timeout=socrata_timeout)


def query(**kwargs):
    log("Executing query: %s" % (json.dumps([kwargs])))
    if showExecutionTimes == 'True':
        start = time.time()
    global client
    try:
        result = client.get(socrata_dataset_identifier,**kwargs)

        log("Saving results")
        logResults(json.dumps(kwargs), json.dumps(result))
    except (ReadTimeout,ReadTimeoutError) as e:
        msg = "Timeout while fetching the data, either optimize the query, or try a higher timeout when connecting"
        log(msg, 'ERROR')
        result = msg
    except HTTPError as e:
        result = e
        log("HTTP Error! %s" % str(str(e).split(":")[0]))
    except Exception as e:
        result = e
        log("Unexpected Error! %s" % str(str(e).split(":")[0]))
    
    if showExecutionTimes == 'True':
        end = time.time()
        log("API call done in %d seconds" % (round(end - start, 2)))
    return result

client = getConnection()