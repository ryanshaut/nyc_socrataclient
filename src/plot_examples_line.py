#!/usr/bin/env python
import plotly.express as px
from utils import *
from api import *

#b = query(query="select count('unique id'), agency_name where 'Created Date' > '2021-07-01' group by agency_name")
b = query(query="select count('unique id'), agency_name group by agency_name")


# b = loadJSONFile('results/87b7a2fd_data.json')
sorted_b = sorted(b,key=lambda x: int(x['count_unique_id']))
fig = px.line(sorted_b, x = 'agency_name', y='count_unique_id')
fig.show()

