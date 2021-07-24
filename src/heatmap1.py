from utils import *
from api import *

q = """
select
 count('unique id'),
 agency_name
 where 
    'Created Date' > '2021-07-01'
group by
    agency_name
"""
query(query=q)