from flask import Flask, request, jsonify  # Make sure Flask is imported
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)  # This line must be present

# Function to fetch data from a URL
def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content
            text_content = soup.get_text()
            # Remove consecutive spaces more than two
            text_content = re.sub(r'\s{2,}', ' ', text_content)
            return text_content.strip()  # Ensure no leading/trailing whitespace
        else:
            return None
    except Exception as e:
        return None

# Main function to be called by Google Cloud Functions
@app.route('/fetch_data', methods=['POST'])  # Define the route and method
def fetch_data():
    request_json = request.get_json(silent=True)

    # Validate incoming data
    if request_json and 'url' in request_json and 'password' in request_json:
        url = request_json['url']  # Now accepting a single URL
        password = request_json['password']

        # Dummy password validation
        if password == "YourPassword123":
            # Fetch data from the URL
            fetched_data = fetch_data_from_url(url)
            if fetched_data:
                return {
                    "Page url": url,  # Include the URL in the response
                    "Page Information": fetched_data  # Return fetched data
                }, 200  # HTTP status code for OK
            else:
                return {"message": f"Failed to fetch data from the URL: {url}"}, 500
            
        else:
            return {"message": "Invalid password."}, 401
    else:
        return {"message": "URL and password are required."}, 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Ensure it listens on the correct port
    app.run(host='0.0.0.0', port=port)  # Start the Flask application
