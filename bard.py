from flask import Flask, redirect, render_template, request, url_for
import requests

class BardImageModel:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def get_image(self, search_query):
        """Searches for an image online and returns the image URL."""
        try:
            # Use the Google Custom Search API to search for the image.
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.search_engine_id}&q={search_query}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors.

            # Extract the image URL from the JSON response if it exists.
            data = response.json()
            items = data.get('items', [])
            if items:
                image_url = items[0]['link']
                return image_url

        except requests.exceptions.RequestException as e:
            # Handle the request exception (e.g., network error, invalid URL, etc.)
            print(f"Error making the API request: {e}")

        # Return None if no valid image URL is found or an error occurs.
        return None

# Create a Flask app.
app = Flask(__name__)

# Replace 'YOUR_API_KEY' and 'YOUR_SEARCH_ENGINE_ID' with your actual values.
api_key = 'AIzaSyANtHaR7aVzQlGaO-5v2ujcs-x5qO8TX84'
search_engine_id ="https://cse.google.com/cse?cx=c2207e8e37d8542b0"

# Create an instance of the BardImageModel.
image_model = BardImageModel(api_key, search_engine_id)

# Define a route to display the search form.
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle the search form submission.
@app.route('/search', methods=['POST'])
def search():
    # Get the user's search query from the form.
    search_query = request.form['query']

    # Redirect to the image generation route with the search query as a parameter.
    return redirect(url_for('generate_image', query=search_query))

# Define a route to generate an image.
@app.route('/generate-image')
def generate_image():
    # Get the search query from the URL parameter.
    search_query = request.args.get('query')

    # Get the image URL from the BardImageModel.
    image_url = image_model.get_image(search_query)

    # Render the image.html template with the image_url variable.
    return render_template('image.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
