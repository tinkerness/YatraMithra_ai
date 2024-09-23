import streamlit as st
from dotenv import dotenv_values  # for loading environment variables
from langchain_google_genai import ChatGoogleGenerativeAI
import requests  # for Unsplash API requests
import os
import pathway as pw
import json
import folium  # for creating maps
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode  # For geocoding


# Load the environment variables from the .env file
env_vars = dotenv_values()

# Fetch the API keys from the environment variables
google_api_key = env_vars.get("GOOGLE_API_KEY")
unsplash_access_key = env_vars.get("UNSPLASH_ACCESS_KEY")
open_cage_api_key = env_vars.get("OPENCAGE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# Initialize the OpenCage Geocoder
geocoder = OpenCageGeocode(open_cage_api_key)

# Define the Prompt for Travel Recommendations
travel_prompt = """
You are a travel guide. Provide a list of top travel locations within or nearby the specified place. Also include details necessary for planning a trip such as suitability for solo travelers, families, or friends, age considerations, weather, terrain, etc.
Place: {}
User preferences: {}
"""

# Functions to Interact with the LLM
# Use the travel prompt to get a list of locations based on the user's preferences
def generate_travel_recommendations(place, preferences):
    try:
        response = llm.invoke(travel_prompt.format(place, preferences))
        print("Travel recommendations generated successfully !")
        return response.content
    except Exception as e:
        st.error(f"Error generating travel recommendations: {e}")
        print(f"Error generating travel recommendations: {e}")
        return None

# Function to fetch an image for a given query from Unsplash
def fetch_image(query, unsplash_access_key):
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {unsplash_access_key}"}
        params = {"query": query, "per_page": 1}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["small"]
        return None
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        print(f"Error fetching image: {e}")
        return None

# Function to get latitude and longitude for a place using OpenCage
def get_lat_lon(place):
    result = geocoder.geocode(place)
    if result and len(result) > 0:
        lat = result[0]['geometry']['lat']
        lon = result[0]['geometry']['lng']
        print("Latitude and Longitude fetched successfully!")
        return lat, lon
    else:
        print("Failed to fetch latitude and longitude.")
        return None, None

# Define a function to create the map
def create_map(place):
    try:
        # Fetch the coordinates for the entered place
        lat, lon = get_lat_lon(place)
        if lat is None or lon is None:
            st.error("Unable to find location coordinates. Please try again.")
            print("Failed to get latitude and longitude.")
        else:
            print(f"Latitude: {lat}, Longitude: {lon}")

            # Create the folium map centered on the place
            m = folium.Map(location=[lat, lon], zoom_start=12)

            # Optionally, add a marker at the location
            folium.Marker([lat, lon], tooltip=f"Location: {place}").add_to(m)

            # Display the map in Streamlit
            st_folium(m, width=700, height=500)
            # st_folium(m)
            print("Map created successfully.")
    except Exception as e:
        st.error(f"Error displaying map: {e}")
        print(f"Error in map creation: {e}")

# Use the Pathway Schema to structure the travel data
class TravelSchema(pw.Schema):
    Location: str
    Suitability: str
    AgeConsiderations: str
    Weather: str
    Terrain: str
    OtherDetails: str
    Image: str

# Save the travel data to a JSON Lines file using Pathway
def save_travel_data(travel_details):
    try:
        # Ensure the data directory exists within the current working directory
        current_dir = os.getcwd()
        output_dir = os.path.join(current_dir, "data")
        os.makedirs(output_dir, exist_ok=True)

        travel_table = pw.Table.from_dict(travel_details, schema=TravelSchema)
        output_path = os.path.join(output_dir, "travel_data.jsonl")
        pw.io.jsonlines.write(travel_table, output_path)
        print(f"Travel data saved successfully at {output_path}")
    except Exception as e:  
        # st.error(f"Error saving travel data: {e}")
        # st.error("Error saving travel data !")
        print(f"Error saving travel data: {e}")

# Load the travel data from the JSON Lines file using Pathway
def load_travel_data():
    try:
        current_dir = os.getcwd()
        input_path = os.path.join(current_dir, "data/travel_data.jsonl")
        print(f"Loading travel data from: {input_path}")
        
        travel_table = pw.io.jsonlines.read(input_path, schema=TravelSchema)
        return travel_table.to_dict()
    except Exception as e:
        # st.error(f"Error loading travel data: {e}")
        st.error("Error loading travel data !")
        print(f"Error loading travel data: {e}")
        return {}


# Define the Streamlit Interface
st.set_page_config(page_title="Yatra Mithra", page_icon="🌍", layout="wide")
st.title("Yatra Mithra 🌍")

# Initialize session state to store user input
if "place" not in st.session_state:
    st.session_state["place"] = ""
if "preferences" not in st.session_state:
    st.session_state["preferences"] = ""
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False

# Text input for the user to enter place and preferences
st.session_state["place"] = st.text_input("Enter a country or place", placeholder="e.g., Paris, France", value=st.session_state["place"])
st.session_state["preferences"] = st.text_area("Enter your travel preferences (e.g., budget, solo, family)", value=st.session_state["preferences"])

# # Text input for the user to enter a place
# place = st.text_input(" Enter a country or place ", placeholder="e.g., Paris, France")
# preferences = st.text_area("Enter your travel preferences (e.g., budget, solo, family)")


# Display the travel recommendations and details
if st.button("Get Travel Recommendations"):
    st.session_state["button_clicked"] = True  # Mark the button as clicked
    # st.session_state.sync()  # Sync the session state to update the button click status
    st.write("Fetching travel recommendations...")

if st.session_state["button_clicked"]:    
    if st.session_state["place"]:
        # Fetch and display image for the entered place
        place_image_url = fetch_image(st.session_state["place"], unsplash_access_key)
        if place_image_url:
            st.image(place_image_url, caption=f"Image of {st.session_state["place"]} from Unsplash", use_column_width=True)
        
        # Generate travel recommendations
        travel_recommendations = generate_travel_recommendations(st.session_state["place"], st.session_state["preferences"])
        st.markdown("### Top Travel Locations")
        st.write(travel_recommendations)

        # Add the dynamic map after travel recommendations
        st.markdown("### Explore the Area on a Map")
        create_map(st.session_state["place"])

        # Create a structured dictionary to save
        travel_details = {
            "Location": st.session_state["place"],
            "Suitability": "General",
            "AgeConsiderations": "All ages",
            "Weather": "Varies",
            "Terrain": "Varies",
            "OtherDetails": travel_recommendations,
            "Image": place_image_url
        }

        # Parse and save the travel data
        try:
            save_travel_data([travel_details])
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
        except Exception as e:
            st.error(f"Error saving travel data: {e}")          
    else:
        st.error("Please enter the name of a place.")


# # Load saved travel data
if st.button("Load Saved Travel Data"):
    st.write("Loading saved travel data...")
    # saved_data = load_travel_data()
    # if saved_data:
    #     st.markdown("### Saved Travel Data")
    #     # st.write(saved_data)
    #     for entry in saved_data:
    #         st.write(entry)
    #         if "Image" in entry and entry["Image"]:
    #             st.image(entry["Image"], caption=entry["Location"], use_column_width=True)
    # else:    
    #     st.error("No saved travel data found.")