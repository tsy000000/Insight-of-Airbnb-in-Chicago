import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

# Read the CSV file
df = pd.read_csv('listings_chicago.csv')

st.title('Chicago Airbnb Insights: Location, Prices, and Amenities')

#Location Analysis (Latitude and Longitude)
st.header('Location Analysis')

map_data = df.loc[:, ["latitude","longitude"]].copy() # use .loc accessor to create a copy
# Rename columns to "lat" and "lon"
map_data = map_data.rename(columns={"latitude": "lat", "longitude": "lon"})
# Create map
map_ = pd.DataFrame(map_data, columns=['lat', 'lon'])
st.write(map_)
st.map(map_,zoom = 10)


# Price Analysis
st.title('Interactive Heat Map of Prices Across Neighborhoods')

# Convert the "price" column to float
df["price"] = df["price"].str.replace(",", "").str.replace("$", "").astype(float)

# Create a new DataFrame with the necessary data
price_data = df.loc[:, ["price", "neighbourhood_cleansed"]]

# Group the data by neighborhood and compute the mean price
price_by_neighborhood = price_data.groupby("neighbourhood_cleansed").mean().reset_index()

# Create the interactive heatmap with Altair
chart = alt.Chart(price_by_neighborhood).mark_rect().encode(
    x=alt.X('price:Q', title='Mean Price'),
    y=alt.Y('neighbourhood_cleansed:O', title='Neighborhood'),
    color='price:Q',
    tooltip=['neighbourhood_cleansed', 'price']
).properties(
    width=800,
    height=600
).interactive()
    
st.altair_chart(chart, use_container_width=True)


# Property analysis (Amenities)
st.header('Property Analysis')

# Convert the amenities column from a string to a list of amenities
bar_data  = df['amenities'].apply(lambda x: x.strip('{}').split(','))

# Create a new DataFrame containing the count of each amenity
amenities_count = pd.Series([item for sublist in bar_data for item in sublist]).value_counts()

print(amenities_count.head(20))

# Create a bar plot of the top 20 amenities with custom x and y labels
fig = px.bar(
    amenities_count.head(20),
    x=amenities_count.head(20).index,
    y=amenities_count.head(20).values,
    labels={
        "x": "Amenities",
        "y": "Count"
    }
)

# Set the title of the plot and make it centered
fig.update_layout(
    title={
        'text': "Top 20 Amenities in Airbnb Chicago",
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title="Amenities",
    yaxis_title="Count"
)

# Display the plot in the Streamlit app
st.plotly_chart(fig)


