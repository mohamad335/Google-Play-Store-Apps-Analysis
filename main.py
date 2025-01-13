import pandas as pd
import plotly.express as px

# Load the dataset
df_app = pd.read_csv('data/apps.csv')

# Clean the dataset by removing rows with missing values
df_clean = df_app.dropna()

# Remove duplicate rows based on 'App', 'Type', and 'Price' columns
df_clean = df_clean.drop_duplicates(subset=['App', 'Type', 'Price'])

# Sort the dataset by 'Rating' in descending order and display the top 5 rows
top_rated_apps = df_clean.sort_values('Rating', ascending=False).head()
# Create a rating value donut chart
rating = df_clean.Content_Rating.value_counts()  # Initialize the data of rating
fig = px.pie(names=rating.index,
             values=rating.values,
             title='Content Rating',
             hole=0.6)

# Update the chart to display the percentage and label outside the donut
fig.update_traces(textposition='outside', textinfo='percent+label')

# Show the chart
fig.show()

