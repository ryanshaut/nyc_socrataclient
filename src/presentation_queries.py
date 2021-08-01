from utils import *
from api import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
client = Api() # bring in the API


### Variables ###
colorMap = {
    'Unspecified' :   'rgba(128,128,0,0.6)',
    'STATEN ISLAND' : 'rgba(128,0,128,0.6)',
    'BRONX' :         'rgba(128,128,128,0.6)',
    'QUEENS' :        'rgba(128,128,200,0.6)',
    'BROOKLYN' :      'rgba(128,200,200,0.6)',
    'N/A' :           'rgba(0,128,0,0.6)',
    'MANHATTAN' :     'rgba(0,0,0,128.6)'
}

totalPopulation = 8336817
population = [
    {'Name': 'STATEN ISLAND' , "Population":  476143 / totalPopulation},
    {'Name': 'BRONX', "Population":  1418207 / totalPopulation},
    {'Name': 'QUEENS', "Population":  2253858 / totalPopulation},
    {'Name': 'BROOKLYN', "Population":  2559903 / totalPopulation},
    {'Name': 'MANHATTAN', "Population":  1628706 / totalPopulation}
]



### End Variables ###

#In[1] # Total Records since 2010

q = """
SELECT
 COUNT('unique id') AS totalCount
WHERE 'Created Date' > '2010-01-01'
"""
res = client.query(query=q)


#In[2] Complaint Types and Noise Complaints break-down

q = """
SELECT
 Complaint_Type,
 COUNT('unique id') AS Count
WHERE  'Created Date' > '2010-01-01'
GROUP BY Complaint_Type
HAVING Count > 1
ORDER BY Count DESC
"""
res = client.query(query=q)
total = sum([int(x['Count']) for x in res.response])
df = list()

for row in res.response:
    row['Percentage'] = int(row['Count']) / total
    df.append(row)
# get just the top 10, then aggregate the remaining into an 'others' category.
top10 = sorted(df, key=lambda x: x['Percentage'], reverse = True)[0:10]
othersPercent = 1 - sum([x['Percentage'] for x in top10])
top10.append({'Complaint_Type': 'All Others', 'Count': '2430930', 'Percentage': othersPercent})

fig = px.pie(top10, values='Percentage', names='Complaint_Type', title='Top 10 Complaint Types')
fig.show()


# Noise complaints on Big Picture and Noise Complaints slides
q = """
SELECT
 Complaint_Type,
 COUNT('unique id') AS count
WHERE 'Created Date' > '2010-01-01'
GROUP BY complaint_type
HAVING count > 1
ORDER BY count DESC
"""
res = client.query(query=q)
noise_complaints = [x for x in res.response if 'noise' in x['Complaint_Type'].lower() ]
df = noise_complaints

fig = px.pie(df, values='count', names='Borough', title='Percent SRs by Borough')
fig.show()

#In[3] Count by Agency
q = """
SELECT
 Agency,
 COUNT('unique id') AS count
 WHERE 'Created Date' > '2010-01-01'
 GROUP BY Agency
 HAVING count > 1
 ORDER BY count DESC
"""
res = client.query(query=q)


#In[4] Count by Borough
q = """
SELECT
 Borough,
 COUNT('unique id') AS count
 WHERE 'Created Date' > '2010-01-01'
 GROUP BY Borough
 HAVING count > 1
 ORDER BY count DESC
"""
res = client.query(query=q)
df = res.response

fig = px.pie(df, values='count', names='Borough', title='Percent SRs by Borough')
fig.show()



#In[5] Count by Year
q = """
SELECT
    date_trunc_y(Created_Date) AS Year,
    COUNT('unique id') AS Count
WHERE 'Created Date' > '2010-01-01'
GROUP BY Year
ORDER BY Year
"""
res = client.query(query=q)
df = res.response

fig = px.line(df, x="Year", y="Count", title='Service Requests per Year')
fig.update_yaxes(type='linear') # this line sorts the y axis!
fig.show()

totalByYear = res.response

for k,v in enumerate(totalByYear):
    totalByYear[k]["Year"] = totalByYear[k]["Year"][0:4]


#In[6] Percentage by Borough per year
q = """
SELECT
    date_trunc_y(Created_Date) AS Year,
    COUNT('unique id') AS Count,
    Borough
WHERE 'Created Date' > '2010-01-01'
GROUP BY Year, Borough
ORDER BY Year, Borough
"""
res = client.query(query=q)
df = res.response

# format the data, add a Borough  key if it's missing, change datetime to just the year, change Count to a percentage of the year
for k,v in enumerate(df):
    if  'Borough' not in df[k]:
        df[k]["Borough"] = "N/A"
    df[k]["Year"] = df[k]["Year"][0:4]
    df[k]['Count'] = int(df[k]['Count']) / int([x['Count'] for x in totalByYear if x['Year'] == df[k]['Year']][0])

fig = go.Figure()

for borough in [x for x in colorMap.keys()]:
    fig.add_trace(go.Bar(
        y=[x['Count'] for x in df if x['Borough'] == borough],
        x=[x['Year'] for x in df if x['Borough'] == borough],
        name= borough,
        marker=dict(
            color=colorMap[borough],
            line=dict(color='rgba(0,128,0, 0.5)', width=0.05),
        )
    ))

fig.update_layout(
        yaxis=dict(
        title_text="Percent(%)",
        ticktext=["0%", "20%", "40%", "60%","80%","100%"],
        tickvals=[0, 20, 40, 60, 80, 100],
        tickmode="array",
        titlefont=dict(size=20),
    ),
    autosize=True,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title={
        'text': "Percent of SRs by Borough by Year",
        'y':0.96,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    barmode='stack')
fig.show()


# In[7] Percent of total SRs by borough compared to borough population

fig = px.pie(population, names = 'Name', values='Population', title='Population by Borough')
fig.show()

q = """
SELECT
 Borough,
 COUNT('unique id') AS count
WHERE 'Created Date' > '2010-01-01'
GROUP BY Borough
HAVING count > 1
ORDER BY count DESC
"""
res = client.query(query=q)
df = res.response

fig = px.pie(df, values='count', names='Borough', title='Percent SRs by Borough')
fig.show()


# In[8] Count of SRs by week of year
q = """
SELECT
 COUNT('unique id') AS Count,
 date_extract_woy(Created_Date) AS WeekOfYear
WHERE 'Created Date' > '2010-01-01'
GROUP BY date_extract_woy(Created_Date)
"""
res = client.query(query=q)
df = res.response

fig=px.line(df, x='WeekOfYear', y='Count' ,title="Service Requests Count by Week of Year")
fig.update_yaxes(type='linear')
fig.show()

# In[9] Count of requests by month, 1 line graph per year

queries = list((
    "Created_Date BETWEEN '2010-01-01' AND '2011-01-01'",
    "Created_Date BETWEEN '2011-01-01' AND '2012-01-01'",
    "Created_Date BETWEEN '2012-01-01' AND '2013-01-01'",
    "Created_Date BETWEEN '2013-01-01' AND '2014-01-01'",
    "Created_Date BETWEEN '2014-01-01' AND '2015-01-01'",
    "Created_Date BETWEEN '2015-01-01' AND '2016-01-01'",
    "Created_Date BETWEEN '2016-01-01' AND '2017-01-01'",
    "Created_Date BETWEEN '2017-01-01' AND '2018-01-01'",
    "Created_Date BETWEEN '2018-01-01' AND '2019-01-01'",
    "Created_Date BETWEEN '2019-01-01' AND '2020-01-01'",
    "Created_Date BETWEEN '2020-01-01' AND '2021-01-01'",
    "Created_Date BETWEEN '2021-01-01' AND '2022-01-01'"
))

q = """
SELECT
 COUNT('unique id') AS Count,
 date_extract_woy(Created_Date) AS WeekOfYear,
 date_extract_y(Created_Date) AS Year
WHERE {0}
GROUP BY date_extract_woy(Created_Date), date_extract_y(Created_Date)
"""
data = list()
for dateQuery in   queries:
    res = client.query(query=str.format(q, dateQuery))
    data.append(res.response)

fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="SR Count by Week of Year per Year")
    ))
for row in data:
    df = row    
    fig.add_trace(go.Scatter(x=[x['WeekOfYear'] for x in df], y=[y['Count'] for y in df], name=df[0]['Year']))

fig.update_yaxes(type='linear', title_text="Count") 
fig.show()

