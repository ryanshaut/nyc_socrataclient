import plotly.express as px
from utils import *
from api import *


b = loadJSONFile('results/87b7a2fd_data.json')
fig = px.scatter(b, x = 'agency_name', y='count_unique_id')
fig.show()

f = extractFromJSON(b)
fig = px.scatter(x = f['agency_name'], y=f['count_unique_id'])
or
fig = px.scatter(f, x = 'agency_name', y='count_unique_id')


# sometimes needed, but not for the above example
fig.update_xaxes(type='category')