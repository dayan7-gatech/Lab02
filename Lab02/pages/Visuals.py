# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

# Read the JSON file
with open(Path(__file__).parent.parent / "data.json", "r") as file:
    data = json.load(file)
    
#Create lists for the data
activities = []
happiness = []
relaxation =[]

for item in data["data_points"]:
    activities.append(item["label"])
    happiness.append(item["happiness_rating"])
    relaxation.append(item["relaxation_rating"])
    
# GRAPH 1: STATIC BAR CHART

st.header("Happiness Rating by Activity")

chart_data = pd.DataFrame({
    "Activity": activities,
    "Happiness Rating": happiness
})

st.bar_chart(
    chart_data,
    x="Activity",
    y="Happiness Rating"
)

st.write("This chart shows the happiness ratings of seven everyday activities.")

# GRAPH 2: DYNAMIC PIE CHART

st.header("Happiness vs. Relaxation")

#Create session state
if "rating_type" not in st.session_state:
    st.session_state.rating_type = "Happiness"
    
# User interaction
st.radio(
    "Choose a rating to display:",
    ["Happiness", "Relaxation"],
    key="rating_type"
)

# Select the data
if st.session_state.rating_type == "Happiness":
    selected_ratings = happiness
else:
    selected_ratings = relaxation
    
# Create advanced pie chart
fig, ax = plt.subplots()

ax.pie(
    selected_ratings,
    labels=activities,
    autopct="%1.1f%%"
)

ax.set_title(st.session_state.rating_type + " Ratings")

st.pyplot(fig)
plt.close(fig)

st.caption("Illustrative ratings on a scale of 1 to 10")

# PART 2: GRAPHS FROM data.csv
st.header("Survey Results")

csv_data = pd.read_csv(Path(__file__).parent.parent / "data.csv")

if not csv_data.empty:
    
    #Graph 3: Stats Pie Chart
    st.subheader("Most Popular Happy Activities 🥇")
    
    activity_counts = csv_data["Category"].value_counts()
    
    fig2, ax2 = plt.subplots()
    
    ax2.pie(
        activity_counts,
        labels=activity_counts.index,
        autopct="%1.1f%%"
    )
    
    ax2.set_title("Activities That Make People Happy 😊")
    
    st.pyplot(fig2)
    plt.close(fig2)
    
    #Graph 4: Dynamic Bar Chart
    st.subheader("Happiness Ratings from Survey")
    
    if "min_happiness" not in st.session_state:
        st.session_state.min_happiness = 1
        
    st.slider(
        "Choose the minimum happiness rating:",
        min_value=1,
        max_value=10,
        key="min_happiness"
    )
    
    filtered_data = csv_data[
        csv_data["Value"] >= st.session_state.min_happiness
    ]
    
    st.bar_chart(
        filtered_data,
        x="Category",
        y="Value"
    )
    
    # Extra Credit: Mean and Median
    st.subheader("Happiness Stats ☀️")

    if not filtered_data.empty:
        mean_rating = filtered_data["Value"].mean()
        median_rating = filtered_data["Value"].median()
        
        if st.session_state.get("previous_mean")is None:
            st.session_state.previous_mean = mean_rating
            
        if st.session_state.get("previous_median") is None:
            st.session_state.previous_median = median_rating
            
        mean_change = mean_rating - st.session_state.previous_mean
        median_change = median_rating - st.session_state.previous_median
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Mean Happiness 😁",
                round(mean_rating, 2),
                delta=round(mean_change, 2)
            )
            
        with col2:
            st.metric(
                "Median Happiness 😃",
                round(median_rating, 2),
                delta=round(median_change, 2)
            )
        
        st.session_state.previous_mean = mean_rating
        st.session_state.previous_median = median_rating
        
    else:
        st.warning("No activities match this rating ⚠️.")
        
        st.session_state.previous_mean = None
        st.session_state.previous_median = None
        
else:
    st.warning("No survey responses yet!‼️")
    
    
