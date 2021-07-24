
from utils import *
from api import *
import plotly.express as px


# get columns in data source
metadata = client.get_metadata(socrata_dataset_identifier)
columns = [x["name"] for x in metadata["columns"]]

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


# this will timeout without adding some additional filters
q = "Fenty"
r = query(q=q,select="agency_name")


q = "Fenty"
r = query(q=q,select="agency_name",where=" 'Created Date' > '2021-07-01'")


q = """
select 
    distinct(agency_name) as AgencyName
 where 
    'Created_Date' > '2021-01-01'
    and 
    agency_name not like "%school%"
"""
query(query=q)



# need to replace spaces in a column with '_' when passing to a functino
q = """
select 
    date_trunc_ymd(Created_Date)
 where 
    'Created_Date' > '2021-07-18'
    and 
    agency_name not like "%school%"
"""
query(query=q)


q = """
select 
 floating_timestamp_day_of_week(to_fixed_timestamp('Created Date')) as thing
  where 
    'Created_Date' > '2021-07-15'
    and 
    agency_name not like "%\school%"
"""
query(query=q)


client.dataset()




# # Going Further
#
# There's plenty more to do! Check out [Queries using SODA](https://dev.socrata.com/docs/queries/) for additional functionality