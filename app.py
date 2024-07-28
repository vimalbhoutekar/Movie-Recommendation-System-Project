from flask import Flask, request, render_template
import pickle
import requests
import aiohttp
import asyncio
import pandas as pd
from flask import jsonify
from collections import OrderedDict

app = Flask(__name__)

movies = pickle.load(open('Model/movies_list.pkl', 'rb'))
similarity = pickle.load(open('Model/similarity_list.pkl', 'rb'))

API_KEY = "694ebd3b6283c17a868004cb14dbcecb"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=694ebd3b6283c17a868004cb14dbcecb"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')
    backdrop_path = data.get('backdrop_path', '')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_popular_movies():
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    popular_movies = []
    for movie in data['results']:
        movie_details = {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'vote_average': movie['vote_average'],
            'id': movie['id']
        }
        popular_movies.append(movie_details)
    return popular_movies

def fetch_popular_people():
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/person/popular?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    popular_people = []
    for person in data['results']:
        person_details = {
            'name': person['name'],
            'profile_path': f"https://image.tmdb.org/t/p/w500/{person['profile_path']}",
            'id': person['id']
        }
        popular_people.append(person_details)
    return popular_people

def fetch_upcoming_movies():
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    upcoming_movies = []
    for movie in data['results']:
        movie_details = {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'vote_average': movie['vote_average'],
            'release_date': movie['release_date'],
            'id': movie['id']
        }
        upcoming_movies.append(movie_details)
    return upcoming_movies

def fetch_top_rated_movies():
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    top_rated_movies = []
    for movie in data['results']:
        movie_details = {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'vote_average': movie['vote_average'],
            'release_date': movie['release_date'],
            'id': movie['id']
        }
        top_rated_movies.append(movie_details)
    return top_rated_movies

def fetch_now_playing_movies():
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    now_playing_movies = []
    for movie in data['results']:
        movie_details = {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'vote_average': movie['vote_average'],
            'release_date': movie['release_date'],
            'id': movie['id']
        }
        now_playing_movies.append(movie_details)
    return now_playing_movies


async def fetch_movie_details(session, movie_id):
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
    async with session.get(movie_url) as response:
        movie_data = await response.json()

    movie_details = {
        "id": movie_id,
        "title": movie_data.get("title", "N/A"),
        "poster_path": f"https://image.tmdb.org/t/p/w500/{movie_data.get('poster_path', '')}",
        "overview": movie_data.get("overview", "N/A"),
        "vote_average": movie_data.get("vote_average", "N/A"),
        "genres": ", ".join([genre["name"] for genre in movie_data.get("genres", [])]),
        "release_date": movie_data.get("release_date", "N/A"),
        "runtime": movie_data.get("runtime", "N/A"),
        "status": movie_data.get("status", "N/A"),
        "cast": []
    }

    for cast_member in movie_data.get("credits", {}).get("cast", [])[:15]:
        cast_details = {
            "id": cast_member.get("id"),  # Include the ID
            "name": cast_member.get("name", "N/A"),
            "character": cast_member.get("character", "N/A"),
            "profile_path": f"https://image.tmdb.org/t/p/w500/{cast_member.get('profile_path', '')}"
        }
        movie_details["cast"].append(cast_details)

    return movie_details


async def fetch_person_details(session, person_id):
    api_key = "694ebd3b6283c17a868004cb14dbcecb"
    url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}&append_to_response=movie_credits"
    
    async with session.get(url) as response:
        data = await response.json()

    person_details = {
        'name': data.get('name', 'N/A'),
        'profile_path': f"https://image.tmdb.org/t/p/w500/{data.get('profile_path', '')}",
        'biography': data.get('biography', 'N/A'),
        'birthday': data.get('birthday', 'N/A'),
        'place_of_birth': data.get('place_of_birth', 'N/A'),
        'movies': []
    }

    for movie in data.get('movie_credits', {}).get('cast', []):
        movie_details = {
            'title': movie.get('title', 'N/A'),
            'poster_path': f"https://image.tmdb.org/t/p/w500/{movie.get('poster_path', '')}" if movie.get('poster_path') else 'https://via.placeholder.com/500x750',
            'id': movie.get('id'),
            'release_date': movie.get('release_date', 'N/A'),
            'vote_average': movie.get('vote_average', 'N/A')
        }
        person_details['movies'].append(movie_details)

    return person_details

async def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_movie_details(session, movies.iloc[i[0]].movie_id) for i in distances[1:11]]
        recommended_movies = await asyncio.gather(*tasks)

    return recommended_movies




@app.route('/')
def home():
    movie_list = movies['title'].values
    return render_template("index.html", movie_list=movie_list)

@app.route('/recommendation', methods=['GET', 'POST'])
async def recommendation():
    movie_list = movies['title'].values.tolist()  # Convert to a regular Python list
    status = False
    error = None
    selected_movie = None
    recommended_movies = []

    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                async with aiohttp.ClientSession() as session:
                    # Fetch details for the selected movie
                    selected_movie_id = movies[movies['title'] == movies_name].movie_id.values[0]
                    selected_movie = await fetch_movie_details(session, selected_movie_id)
                    
                    # Fetch recommendations
                    recommended_movies = await recommend(movies_name)
                status = True
        except Exception as e:
            error = {'error': str(e)}

    return render_template("recommendation.html",
                           movie_list=movie_list,
                           status=status,
                           selected_movie=selected_movie,
                           recommended_movies=recommended_movies,
                           error=error)


@app.route('/movie/<int:movie_id>')
async def movie_details(movie_id):
    async with aiohttp.ClientSession() as session:
        # Fetch movie details
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,images,videos'
        async with session.get(movie_url) as response:
            movie_response = await response.json()

        # Fetch cast details
        cast_details = []
        for member in movie_response['credits']['cast'][:15]:
            person_details = await fetch_person_details(session, member['id'])
            cast_details.append({
                'id': member['id'],
                'name': person_details['name'],
                'profile_path': person_details['profile_path'],
                'character': member['character']
            })

        movie = {
            'id': movie_id,
            'title': movie_response['title'],
            'backdrop_path': f"https://image.tmdb.org/t/p/w1280{movie_response['backdrop_path']}",
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie_response['poster_path']}",
            'overview': movie_response['overview'],
            'vote_average': movie_response['vote_average'],
            'genres': ', '.join([genre['name'] for genre in movie_response['genres']]),
            'release_date': movie_response['release_date'],
            'runtime': movie_response['runtime'],
            'status': movie_response['status'],
            'cast': cast_details,
            'images': [f"https://image.tmdb.org/t/p/w500{image['file_path']}" for image in movie_response['images']['posters'][:8]],
            'backdrops': [f"https://image.tmdb.org/t/p/w1280{image['file_path']}" for image in movie_response['images']['backdrops'][:8]],
            'videos': [{'key': video['key'], 'name': video['name'], 'type': video['type']} for video in movie_response['videos']['results'] if video['site'] == 'YouTube'][:5]
        }

        # Use your custom recommend function
        movie_title = movie_response['title']
        recommended_movies = await recommend(movie_title)

        # Format recommendations
        recommendations = [
            {
                'id': rec['id'],
                'title': rec['title'],
                'poster_path': rec['poster_path'],
                'release_date': rec.get('release_date', ''),
                'vote_average': rec.get('vote_average', 0)
            }
            for rec in recommended_movies
        ]

    return render_template('movie_details.html', movie=movie, recommendations=recommendations)


@app.route('/movie_other/<int:movie_id>')
async def movie_details_other(movie_id):
    async with aiohttp.ClientSession() as session:
        # Fetch movie details
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,images,videos'
        async with session.get(movie_url) as response:
            movie_response = await response.json()

        # Fetch cast details
        cast_details = []
        for member in movie_response['credits']['cast'][:15]:
            person_url = f"https://api.themoviedb.org/3/person/{member['id']}?api_key={API_KEY}"
            async with session.get(person_url) as person_response:
                person_info = await person_response.json()
            cast_details.append({
                'id': member['id'],
                'name': member['name'],
                'character': member.get('character', 'N/A'),
                'profile_path': f"https://image.tmdb.org/t/p/w200{member['profile_path']}" if member['profile_path'] else "https://via.placeholder.com/200x300"
            })

        movie = {
            'id': movie_id,
            'title': movie_response['title'],
            'backdrop_path': f"https://image.tmdb.org/t/p/w1280{movie_response.get('backdrop_path', '')}",
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie_response.get('poster_path', '')}",
            'overview': movie_response.get('overview', 'N/A'),
            'vote_average': movie_response.get('vote_average', 'N/A'),
            'genres': ', '.join([genre['name'] for genre in movie_response.get('genres', [])]),
            'release_date': movie_response.get('release_date', 'N/A'),
            'runtime': movie_response.get('runtime', 'N/A'),
            'status': movie_response.get('status', 'N/A'),
            'cast': cast_details,
            'images': [f"https://image.tmdb.org/t/p/w500{image['file_path']}" for image in movie_response.get('images', {}).get('posters', [])[:10]],
            'backdrops': [f"https://image.tmdb.org/t/p/w1280{image['file_path']}" for image in movie_response.get('images', {}).get('backdrops', [])[:10]],
            'videos': [{'key': video['key']} for video in movie_response.get('videos', {}).get('results', []) if video['site'] == 'YouTube'][:5]
        }

        # Fetch recommendations
        recommendations_url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}'
        async with session.get(recommendations_url) as response:
            recommendations_response = await response.json()
        
        recommendations = []
        for rec_movie in recommendations_response.get('results', [])[:6]:  # Limit to 6 recommendations
            recommendations.append({
                'id': rec_movie['id'],
                'title': rec_movie['title'],
                'poster_path': f"https://image.tmdb.org/t/p/w200{rec_movie['poster_path']}" if rec_movie['poster_path'] else "https://via.placeholder.com/200x300",
                'vote_average': rec_movie.get('vote_average', 'N/A'),
                'release_date': rec_movie.get('release_date', 'N/A'),
            })

    return render_template('movie_details_other.html', movie=movie, recommendations=recommendations)

@app.route('/tv/<int:tv_id>')
async def tv_show_details(tv_id):
    async with aiohttp.ClientSession() as session:
        # Fetch TV show details
        tv_url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={API_KEY}&append_to_response=credits,images,videos'
        async with session.get(tv_url) as response:
            tv_response = await response.json()
            
        # Fetch cast details
        cast_details = []
        for member in tv_response['credits']['cast'][:15]:
            person_url = f"https://api.themoviedb.org/3/person/{member['id']}?api_key={API_KEY}"
            async with session.get(person_url) as person_response:
                person_info = await person_response.json()
            cast_details.append({
                'name': member['name'],
                'character': member.get('character', 'N/A'),
                'profile_path': f"https://image.tmdb.org/t/p/w200{member['profile_path']}" if member['profile_path'] else "https://via.placeholder.com/200x300",
                'id': member['id']
            })

        # Process TV show data
        tv_show = {
            'id': tv_id,
            'name': tv_response['name'],
            'backdrop_path': f"https://image.tmdb.org/t/p/w1280{tv_response.get('backdrop_path', '')}",
            'poster_path': f"https://image.tmdb.org/t/p/w500{tv_response.get('poster_path', '')}",
            'overview': tv_response.get('overview', 'N/A'),
            'vote_average': tv_response.get('vote_average', 'N/A'),
            'genres': ', '.join([genre['name'] for genre in tv_response.get('genres', [])]),
            'first_air_date': tv_response.get('first_air_date', 'N/A'),
            'number_of_seasons': tv_response.get('number_of_seasons', 'N/A'),
            'status': tv_response.get('status', 'N/A'),
            'cast': cast_details,
            'seasons': [],
            'backdrops': [],
            'posters': [],
            'videos': []
        }

        # Process seasons data
        for season in tv_response.get('seasons', []):
            tv_show['seasons'].append({
                'season_number': season['season_number'],
                'episode_count': season['episode_count'],
                'air_date': season.get('air_date', 'N/A'),
                'poster_path': f"https://image.tmdb.org/t/p/w200{season['poster_path']}" if season['poster_path'] else "https://via.placeholder.com/200x300"
            })

        # Process backdrops
        for backdrop in tv_response.get('images', {}).get('backdrops', [])[:10]:
            tv_show['backdrops'].append(f"https://image.tmdb.org/t/p/w1280{backdrop['file_path']}")

        # Process posters
        for poster in tv_response.get('images', {}).get('posters', [])[:10]:
            tv_show['posters'].append(f"https://image.tmdb.org/t/p/w500{poster['file_path']}")

        # Process videos (trailers, teasers, etc.)
        for video in tv_response.get('videos', {}).get('results', []):
            if video['site'] == 'YouTube':
                tv_show['videos'].append({
                    'name': video['name'],
                    'key': video['key'],
                    'type': video['type']
                })
                
        # Fetch recommendations
        recommendations_url = f'https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={API_KEY}'
        async with session.get(recommendations_url) as response:
            recommendations_response = await response.json()
        
        recommendations = []
        for show in recommendations_response.get('results', [])[:6]:  # Limit to 6 recommendations
            recommendations.append({
                'id': show['id'],
                'name': show['name'],
                'first_air_date':show['first_air_date'],
                'poster_path': f"https://image.tmdb.org/t/p/w200{show['poster_path']}" if show['poster_path'] else "https://via.placeholder.com/200x300",
                'vote_average': show.get('vote_average', 'N/A')
            })

        tv_show['recommendations'] = recommendations

    return render_template('tv_show_details.html', tv_show=tv_show)


@app.route('/tv/<int:tv_id>/season/<int:season_number>')
async def season_details(tv_id, season_number):
    async with aiohttp.ClientSession() as session:
        tv_url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={API_KEY}'
        season_url = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={API_KEY}'
        
        async with session.get(tv_url) as response:
            tv_data = await response.json()
        
        async with session.get(season_url) as response:
            season_data = await response.json()
        
        tv_show = {
            'name': tv_data.get('name', 'Unknown Show'),
            'id': tv_id
        }
        
        season = {
            'name': season_data.get('name', f'Season {season_number}'),
            'overview': season_data.get('overview', 'No overview available.'),
            'air_date': season_data.get('air_date', 'N/A'),
            'episode_count': len(season_data.get('episodes', [])),
            'genres': ', '.join([genre['name'] for genre in tv_data.get('genres', [])]),
            'poster_path': f"https://image.tmdb.org/t/p/w300{season_data.get('poster_path')}" if season_data.get('poster_path') else "https://via.placeholder.com/300x450",
            'episodes': []
        }
        
        for episode in season_data.get('episodes', []):
            season['episodes'].append({
                'name': episode.get('name', f'Episode {episode.get("episode_number")}'),
                'overview': episode.get('overview', 'No overview available.'),
                'air_date': episode.get('air_date', 'N/A'),
                'episode_number': episode.get('episode_number', 'N/A'),
                'still_path': f"https://image.tmdb.org/t/p/w300{episode.get('still_path')}" if episode.get('still_path') else "https://via.placeholder.com/300x170"
            })
        
    return render_template('season_details.html', tv_show=tv_show, season=season)



@app.route('/person/<int:person_id>')
def person_details(person_id):
    async def fetch_person():
        async with aiohttp.ClientSession() as session:
            return await fetch_person_details(session, person_id)
    
    person = asyncio.run(fetch_person())
    return render_template('person_details.html', person=person)


@app.route('/popular')
def popular_movies():
    movies = fetch_popular_movies()
    return render_template('popular.html', movies=movies)


@app.route('/upcoming_movies')
def upcoming_movies():
    movies = fetch_upcoming_movies()
    return render_template('upcoming_movies.html', movies=movies)

@app.route('/popular_people')
def popular_people():
    people = fetch_popular_people()
    return render_template('popular_people.html', people=people)

@app.route('/top_rated')
def top_rated():
    movies = fetch_top_rated_movies()
    return render_template('top_rated.html', movies=movies)

@app.route('/now_playing')
def now_playing():
    movies = fetch_now_playing_movies()
    return render_template('now_playing.html', movies=movies)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/suggestions')
async def get_suggestions():
    query = request.args.get('query', '')
    if len(query) < 3:
        return jsonify([])

    async with aiohttp.ClientSession() as session:
        search_url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"
        async with session.get(search_url) as response:
            search_results = await response.json()

    suggestions = []
    for item in search_results.get('results', [])[:5]:  # Limit to top 5 results
        if item['media_type'] in ['movie', 'tv', 'person']:
            suggestions.append({
                'name': item.get('title') or item.get('name'),
                'type': item['media_type'].capitalize(),
                'id': item['id']
            })

    return jsonify(suggestions)



@app.route('/search_results')
async def search_results():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('home'))

    async with aiohttp.ClientSession() as session:
        search_url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"
        async with session.get(search_url) as response:
            search_results = await response.json()

    # Categorize results
    categorized_results = {
        'Movies': [],
        'TV Shows': [],
        'People': []
    }

    total_results = 0

    for item in search_results.get('results', []):
        total_results += 1
        if item['media_type'] == 'tv':
            categorized_results['TV Shows'].append({
                'id': item['id'],
                'name': item['name'],
                'poster_path': item.get('poster_path'),
                'first_air_date': item.get('first_air_date', 'N/A'),
                'vote_average': item.get('vote_average', 'N/A')
            })
        elif item['media_type'] == 'movie':
            categorized_results['Movies'].append({
                'id': item['id'],
                'title': item['title'],
                'poster_path': item.get('poster_path'),
                'release_date': item.get('release_date', 'N/A'),
                'vote_average': item.get('vote_average', 'N/A')
            })
        elif item['media_type'] == 'person':
            categorized_results['People'].append({
                'id': item['id'],
                'name': item['name'],
                'profile_path': item.get('profile_path'),
                'known_for_department': item.get('known_for_department', 'N/A')
            })

    # Count results in each category
    result_counts = {category: len(items) for category, items in categorized_results.items()}
    result_counts = OrderedDict()
    result_counts['All'] = total_results
    for category, items in categorized_results.items():
        result_counts[category] = len(items)
        
    return render_template('search_results.html',
                           categorized_results=categorized_results,
                           result_counts=result_counts,
                           total_results=total_results,
                           query=query)

