# Yatra Mithra 🌍

Yatra Mithra is a travel recommendation web application designed to provide users with top travel locations within or nearby a specified place. It also includes detailed information on each location to assist in trip planning, such as suitability for solo travelers, families, or friends, age considerations, weather, terrain, and more. Additionally, the application fetches images from Unsplash to enhance the travel experience.


## Features

- **Travel Recommendations:** Get a list of top travel locations based on your input.
- **Detailed Information:** Receive detailed information about each location, including suitability, age considerations, weather, terrain, and other details.
- **Image Fetching:** Display images of the specified place and travel locations from Unsplash.
<!-- - **Save and Load Data:** Save travel data to a JSON Lines file and load previously saved data. -->


## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Gemini-pro (for generating travel recommendations)
- **Image Fetching:** Unsplash API
- **Data Processing:** Pathway
- **Data Storage:** JSON Lines


## Prerequisites

- Python 3.12
- Streamlit
- Requests
- Langchain_google_genai
- Pathway
- dotenv


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
    ```


## Usage

1. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```
2. In the browser go to [http://localhost:8501](http://localhost:8501).
3. **Interact with the app:**
    - Enter the name of a country or place in the text input field.
    - Click "Get Travel Recommendations" to see a list of top travel locations and an image of the place.
    - Use the "Load Saved Travel Data" button to view previously saved travel data.


## Demo

![Demo Image](/snips/home.png)
![Demo Image](/snips/hero_img.png)
![Demo Image](/snips/content.png)


## Future Improvements

- **Enhanced Recommendations:** Integrate more detailed and personalized travel recommendations.
- **User Reviews:** Allow users to submit and view reviews for travel locations.
- **Interactive Maps:** Integrate interactive maps to visualize travel locations.
- **Additional APIs:** Incorporate more APIs for additional data sources and features.
- **Multi-language Support:** Add support for multiple languages to cater to a global audience.