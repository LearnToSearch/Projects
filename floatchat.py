import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import re
import random

# Set page configuration
st.set_page_config(
    page_title="FloatChat - ARGO Ocean Data Discovery",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .chat-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        height: 500px;
        overflow-y: scroll;
    }
    .user-message {
        background-color: #d1ecf1;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #f8d7da;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .argo-header {
        background-color: #0c4da2;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #0c4da2;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "argo_data" not in st.session_state:
    st.session_state.argo_data = None

# Generate mock ARGO data
def generate_mock_argo_data():
    # Create dates for the past 5 years
    dates = [datetime.now() - timedelta(days=i) for i in range(0, 1825, 30)]
    
    # Create mock data for different ocean regions
    regions = {
        "North Atlantic": {"lat_range": (20, 45), "lon_range": (-75, -15), "temp_range": (5, 25), "salinity_range": (34.5, 37.5)},
        "South Atlantic": {"lat_range": (-45, -20), "lon_range": (-50, 15), "temp_range": (2, 20), "salinity_range": (34, 36.5)},
        "North Pacific": {"lat_range": (20, 45), "lon_range": (120, 180), "temp_range": (5, 28), "salinity_range": (33.5, 36)},
        "South Pacific": {"lat_range": (-45, -20), "lon_range": (150, 250), "temp_range": (3, 22), "salinity_range": (34, 36.5)},
        "Indian Ocean": {"lat_range": (-35, 20), "lon_range": (40, 120), "temp_range": (10, 30), "salinity_range": (34.5, 36.5)},
        "Arctic Ocean": {"lat_range": (70, 85), "lon_range": (-180, 180), "temp_range": (-2, 5), "salinity_range": (28, 32)},
        "Southern Ocean": {"lat_range": (-75, -45), "lon_range": (-180, 180), "temp_range": (-2, 5), "salinity_range": (33.5, 34.5)}
    }
    
    data = []
    for region, params in regions.items():
        for date in dates:
            for _ in range(5):  # 5 floats per region per month
                lat = random.uniform(*params["lat_range"])
                lon = random.uniform(*params["lon_range"])
                temp = random.uniform(*params["temp_range"])
                salinity = random.uniform(*params["salinity_range"])
                pressure = random.uniform(0, 2000)  # Depth in decibars
                
                data.append({
                    "date": date,
                    "region": region,
                    "latitude": lat,
                    "longitude": lon,
                    "temperature": temp,
                    "salinity": salinity,
                    "pressure": pressure,
                    "float_id": f"ARGO_{region[:3].upper()}_{random.randint(1000, 9999)}"
                })
    
    return pd.DataFrame(data)

# Process user query
def process_query(query):
    query = query.lower()
    response = {"type": "text", "content": "", "data": None}
    
    # Check for greetings
    if any(word in query for word in ["hello", "hi", "hey", "greetings"]):
        response["content"] = "Hello! I'm FloatChat, your ARGO ocean data assistant. How can I help you explore ocean data today?"
        return response
    
    # Check for temperature queries
    if "temperature" in query:
        if "trend" in query or "change" in query:
            # Generate temperature trend data
            df = st.session_state.argo_data
            df['year'] = df['date'].dt.year
            yearly_avg = df.groupby(['region', 'year'])['temperature'].mean().reset_index()
            
            fig = px.line(yearly_avg, x="year", y="temperature", color="region", 
                         title="Ocean Temperature Trends by Region (2018-2023)")
            response["type"] = "plot"
            response["content"] = "Here's the ocean temperature trend by region over the past 5 years:"
            response["data"] = fig
        else:
            # Show current temperature map
            df = st.session_state.argo_data
            recent_data = df[df['date'] > datetime.now() - timedelta(days=30)]
            
            fig = px.scatter_geo(recent_data, lat='latitude', lon='longitude', 
                                color='temperature', hover_name='region',
                                color_continuous_scale='thermal',
                                title='Recent Ocean Temperature Measurements')
            fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                           showland=True, landcolor="lightgray")
            response["type"] = "plot"
            response["content"] = "Here are recent ocean temperature measurements from ARGO floats:"
            response["data"] = fig
    
    # Check for salinity queries
    elif "salinity" in query:
        df = st.session_state.argo_data
        recent_data = df[df['date'] > datetime.now() - timedelta(days=30)]
        
        fig = px.scatter_geo(recent_data, lat='latitude', lon='longitude', 
                            color='salinity', hover_name='region',
                            color_continuous_scale='haline',
                            title='Recent Ocean Salinity Measurements')
        fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                       showland=True, landcolor="lightgray")
        response["type"] = "plot"
        response["content"] = "Here are recent ocean salinity measurements from ARGO floats:"
        response["data"] = fig
    
    # Check for location-specific queries
    elif any(region.lower() in query for region in ["atlantic", "pacific", "indian", "arctic", "southern"]):
        region_map = {
            "atlantic": "Atlantic Ocean",
            "pacific": "Pacific Ocean",
            "indian": "Indian Ocean",
            "arctic": "Arctic Ocean",
            "southern": "Southern Ocean"
        }
        
        for key, region in region_map.items():
            if key in query:
                df = st.session_state.argo_data
                region_data = df[df['region'] == region]
                
                if "temperature" in query:
                    fig = px.scatter(region_data, x='date', y='temperature', 
                                   color='latitude', title=f'Temperature Measurements in {region}')
                    response["type"] = "plot"
                    response["content"] = f"Here are temperature measurements from the {region}:"
                    response["data"] = fig
                elif "salinity" in query:
                    fig = px.scatter(region_data, x='date', y='salinity', 
                                   color='latitude', title=f'Salinity Measurements in {region}')
                    response["type"] = "plot"
                    response["content"] = f"Here are salinity measurements from the {region}:"
                    response["data"] = fig
                else:
                    recent_data = region_data[region_data['date'] > datetime.now() - timedelta(days=30)]
                    fig = px.scatter_geo(recent_data, lat='latitude', lon='longitude', 
                                        color='temperature', hover_name='float_id',
                                        title=f'Recent ARGO Float Measurements in {region}')
                    fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                                   showland=True, landcolor="lightgray")
                    response["type"] = "plot"
                    response["content"] = f"Here are recent measurements from the {region}:"
                    response["data"] = fig
                break
    
    # Check for float information
    elif "float" in query or "argo" in query:
        df = st.session_state.argo_data
        float_ids = df['float_id'].unique()
        selected_float = random.choice(float_ids)
        float_data = df[df['float_id'] == selected_float]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=float_data['date'], y=float_data['temperature'], 
                               name='Temperature', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=float_data['date'], y=float_data['salinity'], 
                               name='Salinity', line=dict(color='blue'), yaxis='y2'))
        
        fig.update_layout(
            title=f'Measurements from ARGO Float {selected_float}',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Temperature (°C)', side='left', color='red'),
            yaxis2=dict(title='Salinity (PSU)', side='right', overlaying='y', color='blue'),
            hovermode='x unified'
        )
        
        response["type"] = "plot"
        response["content"] = f"Here's data from ARGO float {selected_float}:"
        response["data"] = fig
    
    # Default response for unrecognized queries
    else:
        response["content"] = "I can help you explore ARGO ocean data. Try asking about temperature, salinity, or specific ocean regions. For example, you could ask 'Show me temperature trends in the Atlantic Ocean' or 'What is the current salinity in the Pacific?'"
    
    return response

# Main application
def main():
    # Header
    st.markdown("""
    <div class="argo-header">
        <h1>🌊 FloatChat</h1>
        <p>AI-Powered Conversational Interface for ARGO Ocean Data Discovery and Visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize or load ARGO data
    if st.session_state.argo_data is None:
        st.session_state.argo_data = generate_mock_argo_data()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Chat with FloatChat")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message"><b>FloatChat:</b> {message["content"]}</div>', unsafe_allow_html=True)
                    if message.get("plot"):
                        st.plotly_chart(message["plot"], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # User input
        user_input = st.text_input("Type your question about ocean data and press enter:", key="input")
        
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Process query and get response
            response = process_query(user_input)
            
            # Add bot response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response["content"],
                "plot": response["data"] if response["type"] == "plot" else None
            })
            
            # Rerun to update the chat display
            st.rerun()
    
    with col2:
        st.subheader("Ocean Data Overview")
        
        # Show some overview visualizations
        tab1, tab2, tab3 = st.tabs(["Global View", "Temperature", "Salinity"])
        
        with tab1:
            df = st.session_state.argo_data
            recent_data = df[df['date'] > datetime.now() - timedelta(days=30)]
            
            fig = px.scatter_geo(recent_data, lat='latitude', lon='longitude', 
                                color='region', hover_name='float_id',
                                title='Recent ARGO Float Locations')
            fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                           showland=True, landcolor="lightgray")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            df = st.session_state.argo_data
            region_avg = df.groupby('region')['temperature'].mean().reset_index()
            
            fig = px.bar(region_avg, x='region', y='temperature', 
                        title='Average Temperature by Ocean Region')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            df = st.session_state.argo_data
            region_avg = df.groupby('region')['salinity'].mean().reset_index()
            
            fig = px.bar(region_avg, x='region', y='salinity', 
                        title='Average Salinity by Ocean Region')
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer with information about ARGO
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p>The ARGO program is an international collaboration that collects high-quality temperature and salinity profiles from the upper 2000m of the ice-free global ocean.</p>
        <p>This is a prototype interface demonstrating how conversational AI can make ocean data more accessible.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()