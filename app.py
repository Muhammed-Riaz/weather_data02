import streamlit as st
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Function to fetch weather data
def fetch_weather_data():
    """Website se data scrape karega aur CSV me save karega."""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Browser ko background me run karega
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.wunderground.com/dashboard/pws/KKYLOUIS329/table/2025-02-17/2025-02-17/daily"
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    weather_data = []
    
    try:
        table_div = driver.find_element(By.CLASS_NAME, "history-tabs")
        weather_data = table_div.text.split("\n")  # Extract data
        
        # Save data to CSV
        csv_file = "weather_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Weather Data"])  # Header row
            for row in weather_data:
                writer.writerow([row])
        
        st.success("✅ Data saved successfully in CSV!")  # Show success message in Streamlit
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
    
    driver.quit()
    
    return csv_file, weather_data

# 🌟 Streamlit UI
st.title("🌤️ Weather Data Scraper")

if st.button("Fetch Weather Data"):
    with st.spinner("Fetching data... Please wait."):
        csv_file, weather_data = fetch_weather_data()
        
        # Display extracted data
        if weather_data:
            st.subheader("📋 Extracted Weather Data:")
            st.write(weather_data[:10])  # Show first 10 rows
            
            # Provide download button
            with open(csv_file, "rb") as file:
                st.download_button("📥 Download CSV", file, file_name="weather_data.csv", mime="text/csv")
