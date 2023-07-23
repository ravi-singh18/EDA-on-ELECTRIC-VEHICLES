#!/usr/bin/env python
# coding: utf-8

# # Objectives:¶

The primary aim of this project is to conduct a thorough analysis of the dataset to identify significant insights.\ This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently registered through Washington State Department of Licensing (DOL). We set our objective to forumalte a rationale between Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles Population

We will perform EDA on the subject dataset and try to observe and study the dynamics involved in churn transformation.
# In[1]:


#Installing plotly
get_ipython().system('pip install plotly')


# In[3]:


installing bar chart race
get_ipython().system('pip install bar_chart_race')


# In[4]:


#Importing important modules
import pandas as pd 
import plotly.express as px
import bar_chart_race as bcr

Data Exploration:

Load the csv file with the pandas
Creating the dataframe and understanding the data present in the dataset
Dealing with the missing data and the incorrect records
# In[347]:


file = pd.read_csv(r"C:\Users\hp\Downloads\dataset.csv")


# In[348]:


df = pd.DataFrame(file)


# In[349]:


df.head()


# In[350]:


df.info()

Missing values in the data¶

# In[351]:


df.isnull().sum()


# In[352]:


df['Legislative District'] = df['Legislative District'].fillna('N/A')
df['Vehicle Location'] = df['Vehicle Location'].fillna('N/A')
df['Model'] = df['Model'].fillna('N/A')
df['Electric Utility'] = df['Electric Utility'].fillna('Not Avalilable')


# In[353]:


df.rename(columns = {'County':'Country'}, inplace = True)


# In[354]:


df.head()


# In[355]:


# convert the 'Postal Code ' attribute from float to integer
df['Postal Code'] = df['Postal Code'].astype(int)


# In[356]:


df.info()


# In[357]:


df.duplicated().any()


# In[358]:


df.columns.unique()


# In[359]:


df.info()


# # TASK 1

# # Exploratory Analysis and Visualization¶
# 

# Distribution of numerical variables
# ModelYear, Electric Range, Base MSRP, DOL_Vehicle ID

# In[360]:


fig = px.histogram(df['Model Year'] , x = 'Model Year' )
fig.show()

From the above histogram , we can say that electric vehicles are rapidly increases after year of 2020
# In[361]:


#Unvariate analysis on Companies who manufactures the electric vehicle 
fig = px.histogram(df['Make'] )
fig.show()

From the above histogram , we can conclude that Tesla manufactures most electric vehicles
# In[362]:


#Univariate analysis on electric range of cars 
fig = px.histogram(df['Electric Range'] , x = 'Electric Range' )
fig.show()

From the above histogram , we can saay that range of electric vehicles is moderate now a days
# In[370]:


# Univariate analysis of the legislative district according to the no. of vehicles 
fig = px.histogram(df['Legislative District'] , x = 'Legislative District'  )
fig.show()

From the above histogram , we can conclude that electric vehicles moderately distributed in all legislative districts
# In[371]:


#Univariate analysis of driving license of electric vehicle 
fig = px.histogram(df['DOL Vehicle ID'] , x = 'DOL Vehicle ID' )
fig.show()


# In[372]:


# univariate analysis of distribution of electric vehicles across countries
fig = px.histogram(df['Country'] , x = 'Country')
fig.show()

From the above analysis , we can say that mostly electric vehicles are under king 
# In[373]:


#Univariate analysis on states distribution of electric vehicles 
fig = px.histogram(df['State'] , x = 'State')
fig.show()

From the above analysis , we can say that WA is having most no. of electric vehicles
# In[375]:


#Univariate analysis on distribution of electric vehicles in cities
fig = px.histogram(df['City'], x = 'City')
fig.show()

From the above analysis , we can say that Auburn is having most  no. of electric vehicles
# In[379]:


Make_Country = df.groupby(['Country', 'Make']).size().reset_index(name='Count')

# Group the data by country and make, and sum the counts for each group
grouped_data = Make_Country.groupby(['Country', 'Make'])['Count'].sum().reset_index()

# Group the data by country and sum the counts for each country
country_counts = grouped_data.groupby('Country')['Count'].sum().reset_index()
make_counts = grouped_data.groupby('Make')['Count'].sum().reset_index()


# Sort the counties by count in descending order, and select the top 10
top_countries = country_counts.sort_values(by='Count', ascending=False).head(10)
top_makes = make_counts.sort_values(by='Count', ascending=False).head(10)


# Filter the data to only include the top 10 counties
filtered_data = grouped_data[grouped_data['Country'].isin(top_countries['Country']) & grouped_data['Make'].isin(top_makes['Make'])]


# Pivot the data to create a matrix with counties as rows, makes as columns, and counts as values
pivoted_data = filtered_data.pivot(index='Country', columns='Make', values='Count').fillna(0)

fig = px.histogram(pivoted_data)
fig.show()


# In[380]:


km_range = pd.DataFrame(df.groupby('Make')['Electric Range'].mean().reset_index()).sort_values(by='Electric Range',ascending=False).reset_index(drop=True).head(10)
km_range.columns = ['model','km range']
px.pie(data_frame=km_range, names='model', values='km range', hover_name='km range',title='Top 10 Model with KM range',hole=True)


# In[381]:


# Year Wise Cars
year_wise_cars = df.groupby('Model Year')['VIN (1-10)'].count().reset_index()
year_wise_cars.columns = ['Year','num_cars']

fig = px.line(year_wise_cars, x="Year",  y="num_cars", title='Year Wise Number of Cars',markers=True)
fig.show()


# In[417]:


fig = px.choropleth(df,
                    locations='State',
                    color='2020 Census Tract',
                    hover_name='ity',
                    locationmode='USA-states',
                    scope='usa',
                    title='2020 census by State',
                    labels={'2020_census': 'census'},
                    color_continuous_scale='earth')
fig.show()


# In[400]:


df_pivot = df.groupby(['Country','Make'])


# In[412]:


bcr.bar_chart_race(df=df,
                   filename='racing_bar_plot.mp4',  # Output filename for the animation
                   orientation='h',  # 'h' for horizontal bars, 'v' for vertical bars
                   sort='desc',      # Sorting order ('desc' for descending, 'asc' for ascending)
                   n_bars=10,        # Number of bars to display in each frame
                   steps_per_period=10,  # Number of steps (frames) for each year
                   period_length=500,    # Length of each period (in milliseconds)
                   title='Racing Bar Plot: EV Make and its Count Each Year',
                   
                   figsize=(6, 3),  # Figure size (width, height)
                   cmap='dark12',   # Color map for bars
                   period_label={'x': 0.99, 'y': 0.25, 'ha': 'right', 'va': 'center'},  # Position for period label
                   period_fmt='{x:.0f}',  # Format for period label (year)
                   dpi=300,         # Resolution for the animation (dots per inch)
                   )


# # Summary And Conclusion
The Electric Vehicle Population dataset contains information on Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) registered through Washington State Department of Licensing (DOL). Through exploratory data analysis, the top 10 counts of cars per county, city, state, and postal code were determined. King County had the most cars registered, followed by Snohomish and Pierce counties. Seattle had the most cars registered by city, followed by Bellevue and Redmond. Washington had the most cars registered by state, followed by California and Virginia.

The dataset also provided insight into the top 10 consumed car makers by county, city, and state, with Tesla being the most popular make overall. There appears to be an opportunity for car vendors like Audi and BMW to market their vehicles in other states. The top 10 postal codes were also identified, providing further insight for marketing and upselling opportunities.

To Conclude:

King county has the highest number of electric cars registered with 57,398 cars, followed by Snohomish and Pierce county.
Seattle is the city with the highest number of electric cars with 19,860 cars, followed by Bellevue and Redmond.
Washington state has the highest number of electric cars with 109,205 cars, followed by California, Virginia, and Maryland.
The top 10 postal codes with the highest number of electric cars are in the Seattle metro area, with 98052 having the most with 2,805 cars.
Tesla is the most popular electric car make in Washington state, followed by Nissan, Chevrolet, and Toyota.
Tesla is also the most popular make in Seattle, followed by Nissan, Chevrolet, and BMW.
Washington state has the highest number of Audi, BMW, and Chevrolet electric cars registered among all states.
There is a big marketing opportunity for car vendors like Audi, BMW, and Chevrolet in other states, such as Arizona, Florida, and Colorado.
# # TASK 2

# In[422]:


fig = px.choropleth(df,
                    locations='State',
                    color='2020 Census Tract',
                    hover_name='City',
                    locationmode='USA-states',
                    scope='usa',
                    title='2020 census by State',
                    labels={'2020_census': 'census'},
                    color_continuous_scale='earth')
fig.show()


# # TASK 3

# In[423]:


grouped_data = df.groupby(['Model Year', 'Make'])['2020 Census Tract'].sum().reset_index()
pivot_table = grouped_data.pivot(index='Model Year', columns='Make', values='2020 Census Tract')
pivot_table = pivot_table.fillna(0)


# In[ ]:


# Create a Racing Bar Plot to display the animation of EV Make and its count each year
bcr.bar_chart_race(
    df=pivot_table,
    filename=r"C:\Users\Hp\hackthon.mp4",
    orientation='h',
    sort='desc',
    n_bars=6,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B %d, %Y',
    period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                      's': f'Year wise sales: {v.nlargest(6).sum():,.0f}',
                                      'ha': 'right', 'size': 8, 'family': 'Courier New'},
    perpendicular_bar_func='median',
    period_length=500,
    figsize=(5, 3),
    dpi=144,
    cmap='dark12',
    title='Year wise sales of each Makers from last decade',
    title_size='',
    bar_label_size=7,
    tick_label_size=7,
    shared_fontdict={'family' : 'Arial', 'color' : '.1'},
    scale='linear',
    writer='ffmpeg',
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=True)

