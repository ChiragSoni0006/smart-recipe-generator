# Smart Recipe Generator 🍳

A mobile-responsive web application that suggests recipes based on available ingredients. Users can upload photos of their food or manually input ingredients to receive AI-powered recipe suggestions.

## Features
- **Smart Ingredient Matching:** Uses a weighted algorithm to prioritize main ingredients over pantry staples.
- **Image Recognition:** Simulates AI analysis to detect ingredients from uploaded photos.
- **Dietary Filters:** Supports Vegetarian, Vegan, and Gluten-Free filtering.
- **Substitution Logic:** Suggests alternatives for missing ingredients.

## Technical Approach
**Language:** Python 3.9+
**Framework:** Streamlit (chosen for rapid prototyping and built-in mobile responsiveness).

### Key Components:
1.  **Recipe Matching Logic:** I implemented a weighted set intersection algorithm. Core ingredients (proteins, vegetables) carry a weight of 2, while pantry staples (salt, oil) carry a weight of 1. This prevents a recipe from failing simply because the user forgot to list 'salt'.
2.  **Data Storage:** A JSON-based NoSQL approach was used for the MVP to ensure portability and zero-configuration setup.
3.  **Image Processing:** The current implementation uses a mock function to simulate an API response. In a production environment, this function wraps the OpenAI Vision or Google Gemini API.

## Setup & Run
1.  Clone the repository:
    ```bash
    git clone [repo_url]
    ```
2.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Deployment
This app is ready for deployment on **Streamlit Community Cloud**:
1. Push this code to GitHub.
2. Log in to Streamlit Cloud.
3. Select the repository and main file (`app.py`).
4. Click Deploy.