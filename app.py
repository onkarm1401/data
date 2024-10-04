import requests
from bs4 import BeautifulSoup
import re
import os

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
def fetch_data(request):
    request_json = request.get_json(silent=True)

    # Validate incoming data
    if request_json and 'urls' in request_json and 'password' in request_json:
        urls = request_json['urls']
        password = request_json['password']

        # Dummy password validation
        if password == "YourPassword123":
            all_fetched_data = []
            for url in urls:
                # Fetch data from URL
                fetched_data = fetch_data_from_url(url)
                if fetched_data:
                    all_fetched_data.append(fetched_data)  # Append fetched data
                else:
                    return {"message": f"Failed to fetch data from the URL: {url}"}, 500
            
            return {"fetched_data": all_fetched_data}, 200  # Return fetched data as a list
        else:
            return {"message": "Invalid password."}, 401
    else:
        return {"message": "URLs and password are required."}, 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Ensure it listens on the correct port
    app.run(host='0.0.0.0', port=port)
