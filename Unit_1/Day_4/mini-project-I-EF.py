#!/usr/bin/env python
# coding: utf-8

# # Mini-Project I
# During this project, we will practice handling of complex lists and dictionaries in Python. Plus, we will learn how to work with API documentation. Don't be afraid to search for the information in the [**documentation**](https://api.tfl.gov.uk/swagger/ui/index.html?url=/swagger/docs/v1#!/AccidentStats/AccidentStats_Get).
# 
# Let's go to the tasks, we have some parsing to do :)!!

# In[1]:


# import packages we need (remember what packages we used yesterday during the API session)
import requests
import os


# In[48]:


# Set environment variables
get_ipython().run_line_magic('env', "TFL_APP_ID = 'LHL-miniproject'")
get_ipython().run_line_magic('env', 'TFL_PRIMARY_KEY = 78ae8c2021934a69ac8f216eae580894')
get_ipython().run_line_magic('env', 'TFL_SECONDARY_KEY = 65d5b6ac996a46e58969dce63a9c7b55')


# ## Demo

# In[49]:


# Create local variables using our environment variables
# app_id = os.environ["TFL-APP-ID"] - this is not required anymore by TfL
app_key = os.environ["TFL_PRIMARY_KEY"]
url_append = f'?app_key={app_key}' # this will make it easier to append our key to the URL  


# In[50]:


print(url_append)


# In[51]:


# URL
url = "https://api.tfl.gov.uk/AirQuality"
print(url+url_append)


# In[52]:


# We send the request to the API
# NOTE: if you don't have your APP_KEY, run this without the url_append
res = requests.get(url+url_append)


# In[53]:


# We can check if the request was successful - 200 means successful
res.status_code


# In[54]:


# We can export the information that was returned using method .json()
res.json()


# ## Task
# Parse the dictionary and print the AirQuality predictions for tomorrow

# In[30]:


data = res.json() 

# data is a dict, and 'currentForecast' is a key with list values
# the list values in 'currentForecast' are also dict
# so we access the second item (index 1) in 'currentForecast' value
# The key 'forecastText'

tomorrow_summary = data['currentForecast'][1]['forecastSummary']
tomorrow_text = data['currentForecast'][1]['forecastText']
print('Here is the summary of tomorrow\'s forecast:')
print(tomorrow_summary)
# print(tomorrow_text) # Need to figure out how to fix characters


# In[ ]:





# ## Task
# What are the different modes of transport which are operated by Transfer for London? How many of modes do they have?
# 
# Print the list with different modes of transport, plus their count. Example output:
# ```
# [bus, cable-car,.....]
# Number of different modes of transport is: xyz
# ```
# 
# We need to search the documentation for correct request.

# In[36]:


# First, find the API that lists means of transportation
url_mode = 'https://api.tfl.gov.uk/Journey/Meta/Modes'


# In[37]:


# Then, combine the API URL with our API Key
print(url_mode+url_append)


# In[38]:


# Set a new request variable so we don't overwrite the one used for AirQuality
res_mode = requests.get(url_mode+url_append)


# In[42]:


# Check if request was successful
res_mode.status_code


# In[71]:


tfl_services = res_mode.json()
print(tfl_services[0]['isTflService'])


# In[75]:


modes = []

for index in range(len(tfl_services)):
    if tfl_services[index]['isTflService'] == True:
        modes.append(tfl_services[index]['modeName'])

print(modes)


# In[86]:


# First, find the API that lists means of transportation. I used the Journey API
url_mode = 'https://api.tfl.gov.uk/Journey/Meta/Modes'

# Then, combine the API URL with our API Key
#print(url_mode+url_append)

# Set a new request variable so we don't overwrite the one used for AirQuality
res_mode = requests.get(url_mode+url_append)

# Check if request was successful
res_mode.status_code

# Show results in JSON format and assign it to a variable
tfl_services = res_mode.json()
#print(tfl_services[0]['isTflService'])

# Create empty list to store transport modes
modes = []

# for loop that iterates over tfl_services list
# if statement checks if the entry is a TfL service
# if True, the 'modeName' of this entry is appended to modes list
for index in range(len(tfl_services)):
    if tfl_services[index]['isTflService'] == True:
        modes.append(tfl_services[index]['modeName'])

print('The modes of transportation are:', modes)
print('The count of available modes of transportation is:', len(modes) - 1) # Used -1 to remove replacement buses
# Interestingly enough, the TfL website actually shows more modes of transportation than I have here


# ## Task
# How many BikePoints in London are operated by Transfor for London? How many docks are in **all** BikePoints? There is the information for empty and full docks for each BikePoint.

# In[97]:


# First, find the API that lists bike IDs. I used the BikePoint API
url_bike = 'https://api.tfl.gov.uk/BikePoint'

# Test to see if URL and API Key are combined properly
#print(url_mode+url_append)

# Set a new request variable so we don't overwrite the one used for AirQuality
res_bike = requests.get(url_bike+url_append)

# Store request response as a variable
bike_points = res_bike.json()


# In[137]:


# print the list just to find where the data of interest is
# bike_points


# In[175]:


# create a list that will store all BikePoints IDs, then count it 
# to get the number of bike points in London
#point_ids = []

# for loop adds each bike point id to our point_ids list
#for point in range(len(bike_points)):
#    point_ids.append(bike_points[point]['id'])

#print(point_ids)

# Print statement with a count of how many bike points there are 
print('The number of bike points is:', len(bike_points))


# In[126]:


#bike_points[6]['additionalProperties'][8]['value']


# In[136]:


# The line below lets us access the number of docks (NbDocks)
bike_points[0]['additionalProperties'][8]['value']

# Now create an empty variable that will store the total NbDocks
number_docks = 0

# for loop adds each NbDocks to our empty variable
# Since NbDocks is str, we need to convert it to int before we can 
# do basic math

for point in range(len(bike_points)):
    if bike_points[point]['additionalProperties'][8]['value'] == 'false':
        pass
    else: 
        number_docks += int(bike_points[point]['additionalProperties'][8]['value'])

#print(number_docks) - checking
    
# Print statement with a count of how many docks there are 
print('The total number of bike docks is:', number_docks)


# ## Task
# How many tube and bus lines are in London? Print names of all tube lines.

# In[157]:


# For the first part, find the URL that relates to bus and tube lines
url_lines = 'https://api.tfl.gov.uk/Line/Mode/bus,tube'

# Then, combine the API URL with our API Key
#print(url_mode+url_append)

# Set a new request variable so we don't overwrite the one used for AirQuality
res_lines = requests.get(url_lines+url_append)

# Check if request was successful
res_lines.status_code

# Show results in JSON format and assign it to a variable
bt_lines = res_lines.json()
res_lines.json()


# In[159]:


# res_lines is a list where each value is a dict corresponding to a line
# calculating the length of the list should give us the number of tube and bus lines
total_bt_lines = len(bt_lines)

print('The total number of bus and tube lines in London is:', total_bt_lines)


# In[155]:


# For the second part, find the URL that relates to tube lines only
url_tube = 'https://api.tfl.gov.uk/Line/Mode/Tube'

# Then, combine the API URL with our API Key
#print(url_mode+url_append)

# Set a new request variable so we don't overwrite the one used for AirQuality
res_tube = requests.get(url_tube+url_append)

# Check if request was successful
res_tube.status_code

# Show results in JSON format and assign it to a variable
tube_lines = res_tube.json()
res_tube.json()


# In[156]:


# create an empty list that will store tube line names
name_lines = []
# mode_names = [] - this was to check if all entries are for tube lines

# for loop which will access the name of each line, and append to name_lines

for index in range(len(tube_lines)):
    name_lines.append(tube_lines[index]['name'])

print('The London tube line names are:', name_lines)


# ## Task
# How many station has `victoria` line?

# In[165]:


# Find the URL that relates to victoria tube line
url_vic = 'https://api.tfl.gov.uk/Line/Victoria/StopPoints'

# Then, combine the API URL with our API Key
#print(url_mode+url_append)

# Set a new request variable so we don't overwrite the one used for AirQuality
res_vic = requests.get(url_vic+url_append)

# Check if request was successful
res_vic.status_code

# Show results in JSON format and assign it to a variable
vic_stops = res_vic.json()
res_vic.json()


# In[166]:


# vic_stops is a list where each value is a dict corresponding to a stop
# calculating the length of the list should give us the number of tube and bus lines
total_vic_stops = len(vic_stops)

print('The total number of stations in the Victoria line is:', total_vic_stops)


# ## Task
# Plan the journey from Heathrow Airport to Tower Bridge using Bus and Tube? Which way is faster? Example output:
# ```
# Planned duration:
# Bus: x minutes
# Tube: y minutes
# ```
# 
# We need to search the documentation for correct requests and parameters we need.

# In[198]:


# Here, we will calculate how to get to Tower Bridge using the tube (query specifies tube, hence url_t)
url_t = 'https://api.tfl.gov.uk/Journey/JourneyResults/9100HTRWTE4/to/490G00013744?mode=tube'

# Since the API is public, I will not use the API key or appended URL
#print(url_plan+url_append)

# Set a new request variable so we don't overwrite others
res_t = requests.get(url_t)

# Check if request was successful
res_t.status_code

# Show results in JSON format and assign it to a variable
journey_t = res_t.json()
res_t.json()


# In[203]:


# Create empty list which will store duration times for options of tube trips
duration_t = []

# for loops to append the duration times to our empty list
for option in range(len(journey_t['journeys'])):
    duration_t.append(journey_t['journeys'][option]['duration'])

# print the min duration, ie fastest trip
print(min(duration_t))


# In[204]:


# Now, we will calculate how to get to Tower Bridge using buses (query specifies bus, hence url_b)
url_b = 'https://api.tfl.gov.uk/Journey/JourneyResults/9100HTRWTE4/to/490G00013744?mode=bus'

# Since the API is public, I will not use the API key as it is not needed
#print(url_plan+url_append)

# Set a new request variable so we don't overwrite others
res_b = requests.get(url_b)

# Check if request was successful
res_b.status_code

# Show results in JSON format and assign it to a variable
journey_b = res_b.json()
res_b.json()


# In[208]:


# Create empty list which will store duration times for options of bus trips
duration_b = []

# for loops to append the duration times to our empty list
for option in range(len(journey_b['journeys'])):
    duration_b.append(journey_b['journeys'][option]['duration'])

# print the min duration, ie fastest trip
print(min(duration_b))


# In[209]:


print('Planned trip duration:')
print('Bus trip:', min(duration_b), 'minutes')
print('Tube trip:', min(duration_t), 'minutes')

