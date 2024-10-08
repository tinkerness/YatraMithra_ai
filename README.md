# Yatra Mithra 🌍

Yatra Mithra is a travel recommendation web application designed to provide users with top travel locations within or nearby a specified place. It also includes detailed information on each location to assist in trip planning, such as suitability for solo travelers, families, or friends, age considerations, weather, terrain, and more. Additionally, the application fetches images from Unsplash to enhance the travel experience.


## Features

- **Travel Recommendations:** Get a list of top travel locations based on your input place.
- **Personalised Recommendations:** Get filtered travel locations based on your travel preferences.
- **Detailed Information:** Receive detailed information about each location, including suitability, age considerations, weather, terrain, and other details.
- **Image Fetching:** Display images of the specified place and travel locations from Unsplash.
- **Interactive Maps:** Integration of interactive maps to visualize travel locations
<!-- - **Save and Load Data:** Save travel data to a JSON Lines file and load previously saved data. -->


## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Gemini-pro (for generating travel recommendations)
- **Image Fetching:** Unsplash API
- **Interactive Maps:** Folium
- **Geocoding:** OpenCage API
- **Data Processing:** Pathway
- **Data Storage:** JSON Lines


## Prerequisites

- Python 3.12
- Streamlit
- Requests
- Langchain_google_genai
- Pathway
- dotenv
- Folium
- Opencage


## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/yatra-mithra.git
    cd yatra-mithra
    ```
2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv ym-env
    source ym-env/bin/activate  # On Windows: ym-env\Scripts\activate
    ```
3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Set up environment variables:**
    - Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    UNSPLASH_ACCESS_KEY=your_unsplash_access_key
    OPENCAGE_API_KEY=your_opencage_api_key
    ```


## Usage

1. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```
2. In the browser go to [http://localhost:8501](http://localhost:8501).
3. **Interact with the app:**
    - Enter the name of a country or place and the travel preferences in the corresponding text input fields.
    - Click "Get Travel Recommendations" to see a list of top travel locations based on the input preferences along with the image and an interactive map of the place.
    - Use the "Load Saved Travel Data" button to view previously saved travel data.


## Demo

<!-- ![Demo Image](/snips/home.png)
![Demo Image](/snips/hero_img.png)
![Demo Image](/snips/content.png)
[Demo Video](/snips/demo.webm) -->
[demo.webm](https://github.com/user-attachments/assets/f360a0cc-2247-4882-a1cb-ca780da2c352)  

[map.webm](https://github.com/user-attachments/assets/7e2a8446-af8e-4397-a5a2-5461fefac61d)  



<!-- ## Future Improvements

- **User Reviews:** Allow users to submit and view reviews for travel locations.
- **Multi-language Support:** Add support for multiple languages to cater to a global audience. -->
