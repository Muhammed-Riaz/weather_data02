import streamlit as st
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def fetch_weather_data():
    """Website se weather data scrape karega aur CSV me save karega."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode (no GUI)
    options.add_argument("--no-sandbox")  # Streamlit Cloud ke liye zaroori
    options.add_argument("--disable-dev-shm-usage")  # Memory issue fix karega
    options.add_argument("--disable-gpu")  # GPU acceleration disable karega
    options.add_argument("--window-size=1920x1080")  # Proper resolution set karega

    # ChromeDriver setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.wunderground.com/dashboard/pws/KKYLOUIS329/table/2025-02-17/2025-02-17/daily"
    driver.get(url)
    time.sleep(5)  # Page load hone ka wait karega

    weather_data = []
    try:
        table_div = driver.find_element(By.CLASS_NAME, "history-tabs")
        weather_data = table_div.text.split("\n")  # Extract text

        # Save data to CSV
        csv_file = "weather_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Weather Data"])  # Header row
            for row in weather_data:
                writer.writerow([row])

        st.success("✅ Data saved successfully in CSV!")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    driver.quit()
    return csv_file, weather_data

# 🌟 Streamlit UI
st.title("🌤️ Weather Data Scraper")

if st.button("Fetch Weather Data"):
    with st.spinner("Fetching data... Please wait."):
        csv_file, weather_data = fetch_weather_data()
        
        if weather_data:
            st.subheader("📋 Extracted Weather Data:")
            st.write(weather_data[:10])  # Show first 10 rows
            
            # Provide download button
            with open(csv_file, "rb") as file:
                st.download_button("📥 Download CSV", file, file_name="weather_data.csv", mime="text/csv")
