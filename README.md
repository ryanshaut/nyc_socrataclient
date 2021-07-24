# Overview
311 Service Requests from 2010 to Present


Data source:
https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9

# Questions
[] Show number of incidents by date, agency, complaint type, geography, borough
[] Show time to resolution, grouped by various conditions
[] Incidents within a certian distance of a cross street
    [] within distince to landmark



[] How do noise complaints correlate to public holidays
    [] by nonpublic (relegious/ethnic) holidays
        [] by district in NYC
            [] how accurate can we predict a districts ethinic majority by frequency/pattern of noise complaints



# Technical Overview
Download CSV of dataset from https://nycopendata.socrata.com/api/views/erm2-nwe9/rows.csv?accessType=DOWNLOAD
Manual 
https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9 
Export > CSV


https://shautus.sharepoint.com/:x:/r/sites/dev.shaut.us/_layouts/15/Doc.aspx?sourcedoc=%7B35f0fe96-d530-472c-9049-a4879fecb055%7D&action=edit&wdSkeletonState=%7B%22IsEnabled%22%3Atrue%2C%22Options%22%3A1088%7D&wdenableroaming=1&wdorigin=Other&wdredirectionreason=Force_SingleStepBoot&wdinitialsession=38dede06-0343-4057-a33e-d56d58711517&wdrldsc=2&wdrldc=1&wdrldr=ContinueInExcel

Import into SQL via SQL's data import

# API Keys
https://data.cityofnewyork.us/profile/edit/developer_settings

# Pre generated graphs
https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/7ahn-ypff




# References

https://github.com/xmunoz/sodapy

https://dev.socrata.com/blog/2014/11/04/data-visualization-with-python.html