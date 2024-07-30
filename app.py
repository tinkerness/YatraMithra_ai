import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
import pathway as pw
import json
from dotenv import dotenv_values

load_dotenv()

# Load the environment variables from the .env file
env_vars = dotenv_values()

# Fetch the API keys from the environment variables
unsplash_access_key = env_vars.get("UNSPLASH_ACCESS_KEY")
google_api_key = env_vars.get("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)


# Define the Prompt for Travel Recommendations
travel_prompt = """
You are a travel guide. Provide a list of top travel locations within or nearby the specified place. Also include details necessary for planning a trip such as suitability for solo travelers, families, or friends, age considerations, weather, terrain, etc.
Place: {}
"""

# Define Functions to Interact with the LLM
# Use the travel prompt to get a list of locations
def generate_travel_recommendations(place, travel_prompt):
    response = llm.invoke(travel_prompt + place)
    return response.content

# Define function to fetch an image for a given query from Unsplash
def fetch_image(query, unsplash_access_key):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {unsplash_access_key}"}
    params = {"query": query, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data["results"]:
        return data["results"][0]["urls"]["small"]
    return None

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
        # # Convert the list of dictionaries to a Pathway DataFrame
        # travel_df = pw.DataFrame.from_records(travel_details, schema=TravelSchema)

        output_path = os.path.join(output_dir, "travel_data.jsonl")
        pw.io.jsonlines.write(travel_table, output_path)
        # pw.io.jsonlines.write(travel_df, output_path)
    except Exception as e:  
        st.error(f"Error saving travel data: {e}")

# Load the travel data from the JSON Lines file using Pathway
def load_travel_data():
    try:
        current_dir = os.getcwd()
        input_path = os.path.join(current_dir, "data/travel_data.jsonl")
        travel_table = pw.io.jsonlines.read(input_path, schema=TravelSchema)
        return travel_table.to_dict()
        # travel_df = pw.io.jsonlines.read(input_path, schema=TravelSchema)
        # return travel_df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error loading travel data: {e}")
        return {}


# Define the Streamlit Interface
st.set_page_config(page_title="Yatra Mithra", page_icon="🌍", layout="wide")
st.title("Yatra Mithra 🌍")

# Text input for the user to enter a place
place = st.text_input(" Enter the name of a country or place ", placeholder="e.g., Paris, France")


# Display the travel recommendations and details
if st.button("Get Travel Recommendations"):
    if place:
        # Fetch and display image for the entered place
        place_image_url = fetch_image(place, unsplash_access_key)
        if place_image_url:
            st.image(place_image_url, caption=f"Image of {place} from Unsplash", use_column_width=True)
        
        # Get travel recommendations
        travel_recommendations = generate_travel_recommendations(place, travel_prompt)
        st.markdown("### Top Travel Locations")
        st.write(travel_recommendations)
        
        # Create a structured dictionary to save
        travel_details = {
            "Location": place,
            "Suitability": "General",
            "AgeConsiderations": "All ages",
            "Weather": "Varies",
            "Terrain": "Varies",
            "OtherDetails": travel_recommendations,
            "Image": place_image_url
        }

        #     # travel_details = {"Location": locations, "Suitability": "", "AgeConsiderations": "", "Weather": "", "Terrain": "", "OtherDetails": ""}

        # Parse and save the travel data
        try:
            save_travel_data([travel_details])
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
    else:
        st.error("Please enter the name of a place.")

# # Load saved travel data

if st.button("Load Saved Travel Data"):
    saved_data = load_travel_data()
    if saved_data:
        st.markdown("### Saved Travel Data")
        # st.write(saved_data)
        for entry in saved_data:
            st.write(entry)
            if "Image" in entry and entry["Image"]:
                st.image(entry["Image"], caption=entry["Location"], use_column_width=True)
    else:    
        st.error("No saved travel data found.")