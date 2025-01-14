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
rating = df_clean.Content_Rating.value_counts()
def donut_chart_rating(df):
    """
    Create a donut chart to visualize the distribution of content ratings.
    """
    # Initialize the data of rating
    rating = df.Content_Rating.value_counts()
    
    # Create the pie chart
    fig = px.pie(names=rating.index,
                 values=rating.values,
                 title='Content Rating',
                 hole=0.6)
    
    # Update the chart to display the percentage and label outside the donut
    fig.update_traces(textposition='outside', textinfo='percent+label')
    
    # Show the chart
    fig.show()
#convert Installs to numeric
df_clean.Installs = df_clean.Installs.astype(str).str.replace(',', "")
df_clean.Installs = pd.to_numeric(df_clean.Installs)
df_clean[['App', 'Installs']].groupby('Installs').count()
#convert Price to numeric
df_clean.Price = df_clean.Price.astype(str).str.replace('$', '')
df_clean.Price = pd.to_numeric(df_clean.Price)
df_clean[['App', 'Price']].groupby('Price').count()
# Remove rows with 'Price' greater than 250
df_clean = df_clean[df_clean['Price'] < 250]
df_clean.sort_values('Price', ascending=False).head(5)
 # Group the data by 'Category' and calculate the total number of installs
category_installs = df_clean.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values('Installs', ascending=True, inplace=True)
def category_revenue(df):
    df_clean.to_csv('data/apps_clean.csv', index=False)
    #top 10 categories with highest revenue estimate
    top10_category = df_clean.Category.value_counts()[:10]
    # Create a bar chart to visualize the top 10 categories with the highest revenue estimate
    fig = px.bar(x=top10_category.index, y=top10_category.values)
    fig.update_layout(title='Top 10 Categories by Revenue Estimate', xaxis_title='Category', yaxis_title='Revenue Estimate')
    fig.write_image('images/top_10_category.png')
    fig.show()

def category_popularity(df):
    """
    Create a bar chart to visualize the popularity of categories.
    """
   
    # Create a horizontal bar chart
    h_bar = px.bar(x = category_installs.Installs,
               y = category_installs.index,
               orientation='h',
               title='Category Popularity')
 
    h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
    h_bar.write_image('images/category_popularity.png')
    h_bar.show()
def category_concentration(df):
    """
    create a scatter plot to visualize the category concentration.
    """
    #group number of apps in each category
    category_concentration = df_clean.groupby('Category').agg({'App': pd.Series.count})
    #merge the twwo dataframes
    merged_df = category_installs.merge(category_concentration, on='Category', how='inner')

    # Create a scatter plot
    scatter = px.scatter(merged_df, # data
                    x='App', # column name
                    y='Installs',
                    title='Category Concentration',
                    size='App',
                    hover_name=merged_df.index,
                    color='Installs')
 
    scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                      yaxis_title="Installs",
                      yaxis=dict(type='log'))
    scatter.write_image('images/category_concentration.png')
 
    scatter.show()
def top_geners(df):
    """create a bar chart to visualize the top genres."""
    geners= df_clean.Genres.str.split(';', expand=True).stack()
    num_geners = geners.value_counts()
    bar= px.bar(x=num_geners.index[:15]
                ,y=num_geners.values[:15]
                ,title='Top Genres'
                ,hover_name=num_geners.index[:15]
                ,color=num_geners.values[:15]
                ,color_continuous_scale='Agsunset')
    bar.update_layout(xaxis_title='Genres', yaxis_title='Number of Apps', coloraxis_showscale=False)
    bar.write_image('images/top_geners.png')
    bar.show()

top_geners(df_clean)
    
