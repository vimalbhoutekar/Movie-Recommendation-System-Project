# Movie Recommendation System

## Project Overview

The **Movie Recommendation System** is a content-based movie recommendation system that uses bag-of-words vectorization and cosine similarity. This system suggests movies based on the content and features of the movies already liked by the user. It is designed to help users discover new movies that match their tastes and preferences.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots and Videos](#screenshots-and-videos)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Content-Based Filtering**: Recommends movies based on their content by analyzing features such as plot, genre, cast, and crew.
- **Bag-of-Words Vectorization**: Converts textual movie descriptions into numerical vectors, allowing for similarity comparisons.
- **Cosine Similarity**: Measures the cosine of the angle between two vectors, enabling the calculation of similarity between movies.
- **User-Friendly Interface**: Built with Flask, the web interface is simple and intuitive, providing a seamless user experience.
- **Real-Time Recommendations**: Users receive instant movie recommendations based on their input.

## Installation

To set up the Movie Recommendation System locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/vimalbhoutekar/Movie-Recommendation-System-Project.git
    cd Movie-Recommendation-System-Project
    ```

2. **Create and activate a virtual environment:**

   On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

   On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

## Usage

After installing the system, follow these steps to use it:

1. Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).
2. Enter the name of a movie you like in the search bar.
3. Get instant recommendations for similar movies.

## Screenshots and Videos

### Screenshots

### Home Page
![home page 1](https://github.com/user-attachments/assets/d6986881-6164-4eab-99aa-c9c96c2a7126)
![home page 2](https://github.com/user-attachments/assets/de80983f-d65f-4a36-8543-e58e43f9c20a)
![home page 3](https://github.com/user-attachments/assets/fe7d922e-d6f0-46da-b17f-7070dd4675df)

### Recommendations Page
![recom1](https://github.com/user-attachments/assets/04dd77f0-f0af-4caf-ad30-7c33d23c78e9)

![recom2](https://github.com/user-attachments/assets/dacfdea7-480d-48a7-a26d-fbaabd8e2785)
![recom 3](https://github.com/user-attachments/assets/29f2ea0e-cc3e-4c01-a703-f9aa68a96a70)
![recom 4](https://github.com/user-attachments/assets/da0b7153-2fa1-4ec2-b1c4-f7eafcd59ec8)
![recom 5](https://github.com/user-attachments/assets/79be2cad-1acc-4c93-81ef-af1916201b35)
![recom 6](https://github.com/user-attachments/assets/74db8d30-d28b-4ca6-8a4a-5b0e13ed7b55)

### Videos

#### Video Demo
[Check out our video demo](static/Images/video_demo.mp4) to see the Movie Recommendation System in action!

## Files

- `app.py` - The main Python file that runs the Flask application.
- `Dataset/` - Folder containing dataset files:
  - `tmdb_5000_credits.csv` - Contains information about movie credits (cast and crew).
  - `tmdb_5000_movies.csv` - Contains information about movies (title, genres, plot, etc.).
- `Model/` - Folder containing model files:
  - `movies_list.pkl` - Pickle file containing the list of movies.
  - `similarity_list.pkl` - Pickle file containing the precomputed similarity matrix.
- `static/` - Folder containing static files like CSS, JavaScript, and images.
  - `Images/` - Contains images used in the project.
  - `Script/` - Contains JavaScript files.
  - `Style/` - Contains CSS files.
- `templates/` - Folder containing HTML templates for the web pages:
  - `about.html` - About page of the web application.
  - `index.html` - Home page of the web application.
  - `movie_details.html` - Page displaying details of a selected movie.
  - `movie_details_other.html` - Another template for displaying movie details.
  - `now_playing.html` - Page displaying currently playing movies.
  - `person_details.html` - Page displaying details of a person (actor/actress).
  - `popular.html` - Page displaying popular movies.
  - `popular_people.html` - Page displaying popular actors and actresses.
  - `recommendation.html` - Page displaying movie recommendations.
  - `search_results.html` - Page displaying search results.
  - `season_details.html` - Page displaying details of a TV show season.
  - `top_rated.html` - Page displaying top-rated movies.
  - `tv_show_details.html` - Page displaying details of a TV show.
  - `upcoming_movies.html` - Page displaying upcoming movies.
- `requirements.txt` - File listing all dependencies required for the project.
- `Movie Recommendation System.ipynb` - Jupyter notebook for the movie recommendation system.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/YourFeature`)
3. **Commit your Changes** (`git commit -m 'Add Your Feature'`)
4. **Push to the Branch** (`git push origin feature/YourFeature`)
5. **Open a Pull Request**

## License

Distributed under the MIT License. See `LICENSE` for more information.

**Developed by Vimal Bhoutekar**
