import requests
import streamlit as st
import base64
import time
import pickle
import http
# Function to load and encode the image in base64
def get_base64_of_bin_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

if "prediction_submitted" not in st.session_state:
    st.session_state.prediction_submitted = False

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

if "live_data" not in st.session_state:
    st.session_state.live_data = {}

nb=pickle.load(open("model_file.pkl","rb"))
nb2=pickle.load(open("model_file1.pkl","rb"))
nb3=pickle.load(open("model_file7.pkl","rb"))
nb4=pickle.load(open("model_file8.pkl","rb"))
wh=pickle.load(open("weather.pkl","rb"))
tab1, tab2 ,tab3 = st.tabs(["Historical Data", "Live Data","Results"])

# Provide the path to your local image
image_file_path = "photo4.jpg"  # Replace with your image file path

# Encode the image
base64_img = get_base64_of_bin_file(image_file_path)

# CSS for setting the background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{base64_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""
st.sidebar.subheader("Welcome to SKY WATCHER")
st.sidebar.write("Welcome to the Rain Predictor web application! This platform leverages the power of Machine Learning and live weather data to provide accurate predictions on whether it will rain tomorrow.")
st.sidebar.write("Key Feature: ")
st.sidebar.write("1. Custom Weather Data Predictions:")
st.sidebar.write("Upload your own weather data (e.g., temperature, humidity, wind speed) to predict if it will rain tomorrow.")
st.sidebar.write("2. Live Weather Updates:")
st.sidebar.write("Enter your city, and the application will fetch live weather data using the OpenWeather API, based on real-time data, it will predict if it’s likely to rain tomorrow in your location.")


tod_rain=["No", "Yes"]
tom_rain=["No", "Yes"]

direction_to_degree = {
    'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90,
    'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
    'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270,
    'WNW': 292.5, 'NW': 315, 'NNW': 337.5
}

with tab1:
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("Welcome to SKY WATCHER")

    # Sidebar Header
    #st.sidebar.header("Tomorrow’s Sky")

    with st.form(key="rainfall_form"):
        # Input sliders and dropdown
        min_temp = st.slider("Minimum Temperature (°C)", -5, 22, 0)
        max_temp = st.slider("Maximum Temperature (°C)", 6, 36, 6)
        wind_dir = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        wind_speed = st.slider("Wind Speed (km/h)", 0, 100, 10)
        humidity = st.slider("Humidity (%)", 0, 100, 50)
        pressure = st.slider("Pressure (hPa)", 900, 1100, 1013)
        temp = st.slider("Temperature (°C)", -10, 40, 25)
        today_rain = st.selectbox("Raining Today ", ["No", "Yes"])
                
        # Form submission
        submit_button = st.form_submit_button("Predict Rainfall")
            
    # Handle form submission
    if submit_button:
        # Dummy prediction logic (replace with your ML model)
        #will_rain = "Yes" if humidity > 70 and today_rain == "Yes" else "No"
                
        # Store the form data and prediction result in session state
        with st.spinner("Processing your input..."):
            time.sleep(2)  # Simulate a delay (e.g., for a prediction model)
                
            # Store the form data in session state
            st.session_state.form_data = {
                "min_temp": min_temp,
                "max_temp": max_temp,
                "wind_dir": wind_dir,
                "wind_speed": wind_speed,
                "humidity": humidity,
                "pressure": pressure,
                "temp": temp,
                "today_rain": today_rain,
            }
        success_message = st.success("Form submitted successfully!")
        time.sleep(5)  # Keep the success message for 5 seconds
        success_message.empty() 
        

with tab2:
    API_KEY = '0b2c53904c2ef8464b5011ffd22c7807'

    def fetch_lat_long(city):
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            lat_long = {
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
        }
        return lat_long

    def fetch_weather_forecast(lat,long):
        url2=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}&unit=metric"
        response2 = requests.get(url2)
        if response2.status_code == 200:
            data2 = response2.json()
            weather_features = {
            'temperature1':round(data2['main']['temp']) ,
            'min_temp1' : round(data2['main']['temp_min']),
            'max_temp1': round(data2['main']['temp_max'] ) ,
            'humidity1': round(data2['main']['humidity']),
            'pressure1': round(data2['main']['pressure']),
            'wind_speed1': round(data2['wind']['gust']) ,
            'wind_dir1' : round(data2['wind']['deg']) ,
            'main':data2["weather"][0]["main"]
            }
            return weather_features
        else:
            raise Exception("Error fetching weather data!")
        
    st.title("Make Prediction with the live data !!")
    city = st.text_input("City Name:", placeholder="Enter City Name")
    b=st.button("Get Prediction",key=4)
    if b:
        lat_lon=fetch_lat_long(city=city)
        lat=lat_lon['lat']
        long=lat_lon['lon']
        st.session_state.live_data=fetch_weather_forecast(lat=lat,long=long)
        sos=st.success("Input Fetch Successfully See Result On Result Tab") 
        time.sleep(5)  # Keep the success message for 5 seconds
        sos.empty()
       

with tab3:
    st.title("Prediction Result")
    
    if st.session_state.live_data:
        st.subheader("Your Submitted Data:")
        for key, value in st.session_state.live_data.items():
            st.write(f"**{key.replace('_', ' ').title()}**: {value}")
        
        # Additional title after displaying the data
        st.title("Prediction: ")
        res1=nb2.predict([[st.session_state.live_data['min_temp1'], st.session_state.live_data['max_temp1'],st.session_state.live_data['wind_dir1'],st.session_state.live_data['wind_speed1'],st.session_state.live_data['humidity1'],st.session_state.live_data['pressure1'],st.session_state.live_data['temperature1']]])
        st.markdown(f"**PREDICTION:** {tom_rain[res1[0]]}")
        #tom_rain[res1[0]]
        result= {tom_rain[res1[0]]}
        if result=="Yes":
            st.success("It will rain today")
        else:
            st.error("It will not rain today")
        
        st.session_state.form_data={}
           
    elif st.session_state.form_data:
        st.subheader("Your Submitted Data:")
        
        # Loop through the form data and display each key-value pair
        for key, value in st.session_state.form_data.items():
            st.write(f"**{key.replace('_', ' ').title()}**: {value}")
        st.title("Prediction: ")
        res=wh.predict([[min_temp, max_temp,direction_to_degree[wind_dir],wind_speed,humidity,pressure,temp,tod_rain.index(today_rain)]])
        result= {tom_rain[res[0]]}
        if result=="Yes":
            st.success("It will rain today")
        else:
            st.error("It will not rain today")
        
        st.session_state.form_data={}

            
    else:
        st.warning("No data submitted yet. Please fill out the form in Tab 1.")