import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 🧾 Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Zomato Data Analysis", layout="wide")
st.title("🍽️ Zomato Data Analysis Dashboard")
st.markdown("### Explore restaurant trends interactively using Streamlit + Plotly")

# ------------------------------------------------------------
# 📂 Load Data
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("zomato.csv", encoding='latin1')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

df = load_data()
st.success("✅ Zomato dataset loaded successfully!")

# ------------------------------------------------------------
# 🧹 Data Cleaning
# ------------------------------------------------------------
if 'restaurant_id' in df.columns:
    df.drop_duplicates(subset='restaurant_id', inplace=True)

drop_cols = [c for c in ['city', 'cuisines', 'aggregate_rating'] if c in df.columns]
df.dropna(subset=drop_cols, inplace=True)

# ------------------------------------------------------------
# 🔍 Sidebar Filters
# ------------------------------------------------------------
st.sidebar.header("🔍 Filters")

if 'city' in df.columns:
    cities = sorted(df['city'].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "Select Cities", cities, default=cities[:5]
    )
    if selected_cities:
        df = df[df['city'].isin(selected_cities)]

# ------------------------------------------------------------
# 📊 Key Metrics
# ------------------------------------------------------------
st.subheader("📈 Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Restaurants", len(df))
col2.metric("Average Rating", round(df['aggregate_rating'].mean(), 2))
col3.metric("Total Votes", int(df['votes'].sum()) if 'votes' in df.columns else 0)
col4.metric("Avg Cost for Two", int(df['average_cost_for_two'].mean()) if 'average_cost_for_two' in df.columns else 0)

st.divider()

# ------------------------------------------------------------
# 🏙️ Top 10 Cities by Restaurant Count
# ------------------------------------------------------------
if 'city' in df.columns:
    city_count = df['city'].value_counts().head(10).reset_index()
    city_count.columns = ['city', 'count']
    fig1 = px.bar(city_count,
                  x='city', y='count', color='city',
                  title="🏙️ Top 10 Cities by Number of Restaurants",
                  labels={'city': 'City', 'count': 'Restaurant Count'})
    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------
# 🍕 Top 10 Cuisines
# ------------------------------------------------------------
if 'cuisines' in df.columns:
    cuisine_count = df['cuisines'].value_counts().head(10).reset_index()
    cuisine_count.columns = ['cuisine', 'count']
    fig2 = px.bar(cuisine_count,
                  x='cuisine', y='count', color='cuisine',
                  title="🍕 Top 10 Cuisines",
                  labels={'cuisine': 'Cuisine', 'count': 'Count'})
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# ⭐ Rating Distribution
# ------------------------------------------------------------
fig3 = px.histogram(df, x='aggregate_rating', nbins=20,
                    title="⭐ Rating Distribution", color_discrete_sequence=['#00CC96'])
st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------------------
# 💸 Rating vs Cost Scatter
# ------------------------------------------------------------
if {'average_cost_for_two', 'aggregate_rating'}.issubset(df.columns):
    fig4 = px.scatter(df,
                      x='average_cost_for_two', y='aggregate_rating',
                      color='city' if 'city' in df.columns else None,
                      size='votes' if 'votes' in df.columns else None,
                      hover_data=['cuisines'],
                      title="💸 Rating vs Average Cost for Two")
    st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------------------------------
# 🗳️ Votes vs Rating Scatter
# ------------------------------------------------------------
if 'votes' in df.columns:
    fig5 = px.scatter(df,
                      x='votes', y='aggregate_rating',
                      color='city' if 'city' in df.columns else None,
                      title="🗳️ Votes vs Rating")
    st.plotly_chart(fig5, use_container_width=True)

# ------------------------------------------------------------
# 💰 Price Range vs Average Rating
# ------------------------------------------------------------
if 'price_range' in df.columns:
    price_rating = df.groupby('price_range')['aggregate_rating'].mean().reset_index()
    fig6 = px.bar(price_rating,
                  x='price_range', y='aggregate_rating',
                  title="💰 Average Rating by Price Range",
                  labels={'price_range': 'Price Range', 'aggregate_rating': 'Average Rating'},
                  color='aggregate_rating')
    st.plotly_chart(fig6, use_container_width=True)

# ------------------------------------------------------------
# 🗺️ Restaurant Map
# ------------------------------------------------------------
if {'latitude', 'longitude'}.issubset(df.columns):
    fig7 = px.scatter_mapbox(df,
                             lat='latitude', lon='longitude',
                             hover_name='restaurant_name' if 'restaurant_name' in df.columns else None,
                             hover_data=['city', 'cuisines', 'aggregate_rating'],
                             color='aggregate_rating',
                             color_continuous_scale='RdYlGn',
                             zoom=3, height=500)
    fig7.update_layout(mapbox_style='open-street-map')
    fig7.update_layout(title="🗺️ Restaurant Locations Map")
    st.plotly_chart(fig7, use_container_width=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.divider()
st.markdown("📊 *Built with Streamlit + Plotly — Zomato Data Analysis Dashboard*")
