import os
import requests
from flask import Flask, render_template, request, redirect, session
import random
from flask_caching import Cache
import uuid

app = Flask(__name__)

# key for managing sessions (managing cookies)
app.secret_key = os.urandom(24)

# creating a cache to store playlists data later on
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 600
cache = Cache(app)


@app.route('/')
def index():
    session.clear()
    return render_template("index.html")
    # rendering the base template for user upon opening the page

# route upon entering playlist URL


@app.route('/quiz', methods=['POST'])
def quiz():
    # getting user input
    playlist_url = request.form.get('playlist_url')

    # if user does not provide anything we return to index page
    if not playlist_url:
        return redirect("/")

    # if user provided something we try to extract the playlist
    try:
        # extracting just the playlist ID
        playlist_id = playlist_url.split('/')[-1]
        #print(f"Extracted Playlist ID: {playlist_id}")

        if not playlist_id.isdigit():
            return redirect("/")

        # constructing api url to make requests, sending the requests and checking for errors
        tracks_url = (f"https://api.deezer.com/playlist/{playlist_id}/tracks")
        playlist_url = (f"https://api.deezer.com/playlist/{playlist_id}")

        response_tracks = requests.get(tracks_url)
        response_playlist = requests.get(playlist_url)

        response_tracks.raise_for_status()
        response_playlist.raise_for_status()

        # parsing json response from api, we got our response!
        tracks_data = response_tracks.json()
        playlist_data = response_playlist.json()

        # validating our data, if incorrect or empty we just go back to index page
        if not tracks_data or not playlist_data or 'data' not in tracks_data or not tracks_data['data']:
            return redirect("/")

        # we have our data, now we just filter the things that we'll need later
        # creating a new dictionary of items required to get our quiz working
        # it covers name of the song, its artist and URL to play music, if it doesn't exist we just filter out that song
        tracks = [
            {
                'name': item['title_short'],
                'artist': item['artist']['name'],
                'preview_url': item['preview']
            }
            for item in tracks_data['data'] if 'preview' in item and item['preview']
        ]

        while 'next' in tracks_data:
            tracks_url = tracks_data['next']
            response_tracks = requests.get(tracks_url)
            response_tracks.raise_for_status()
            tracks_data = response_tracks.json()
            temp_tracks = [
                {
                    'name': item['title_short'],
                    'artist': item['artist']['name'],
                    'preview_url': item['preview']
                }
                for item in tracks_data['data'] if 'preview' in item and item['preview']
            ]
            tracks.extend(temp_tracks)

        if not tracks:
            return redirect("/")

        # in order to transfer data across pages we both cookies (session dictionary) and cache (and its ID that we store in cookies)
        playlist_uuid = str(uuid.uuid4())
        # uuid that we'll store in cookies, also used as our key in cache
        cache.set(playlist_uuid, tracks)
        session['playlist_uuid'] = playlist_uuid
        # as normal cookies could not fit bigger playlists, I decided to go with cache

        session['playlist_title'] = playlist_data['title']
        session['playlist_image'] = playlist_data['picture_big']

    # if format is incorrect we go back to index page
    except IndexError:
        return redirect("/")

    # if api requests throws exceptions we go back to index page
    except requests.exceptions.RequestException as e:
        return redirect("/")

    # If the request was successful we print data to terminal
    #print("Playlist data fetched successfully!")

    return redirect("/settings")

# helper function to get a quiz question - either about title or artist of a given track


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get("playlist_uuid"):
        return redirect("/")

    if request.method == "GET":
        tracks = cache.get(session.get("playlist_uuid"))
        return render_template("settings.html", playlist_title=session.get("playlist_title"), playlist_image=session.get("playlist_image"), max_tracks=(len(tracks)-1))
    # get request renders our page
    else:
        # getting settings back from user
        track_count = request.form.get("track_count", type=int)
        round_duration = request.form.get("round_duration", type=int)
        question_types = request.form.get("question_types")

        tracks = cache.get(session.get("playlist_uuid"))
        tracks_len = len(tracks)
        # if anything is missing or incorrect then we returect user back to settings again
        if track_count < 1 or track_count > tracks_len or round_duration < 10 or round_duration > 30:
            return redirect("/settings")

        # if everything is valid then we save it to session data and go to quiz_page
        session["question_types"] = question_types
        session["track_count"] = track_count
        session["total_questions"] = track_count
        session["round_duration"] = round_duration
        session["score"] = 0

        return redirect("/quiz_page")


def get_quiz_question():
    # First we get back playlist_uuid from cookies, then list of tracks
    playlist_uuid = session.get("playlist_uuid")

    if not playlist_uuid:
        return None

    tracks = cache.get(playlist_uuid)

    # if tracks is empty then user did not submit a correct playlist, we give no answer
    if not tracks:
        return None

    # We select a random track for our quiz purposes
    current_track = random.choice(tracks)

    # getting question type from settings (artists, titles, both)
    question = session.get("question_types")

    # if it's not only artists or only titles then we choose randomly (as well as when user types something on his own)
    if question not in ["artist", "title"]:
        # we get our random choice of question type
        question = random.choice(["artist", "title"])

    if question == "artist":
        # getting a full list of artists
        options = list(set([track["artist"] for track in tracks]))
        correct_answer = current_track["artist"]
        question_text = "Who is the artist of this song?"
    else:
        # getting a full list of titles
        options = list(set([title["name"] for title in tracks]))
        correct_answer = current_track["name"]
        question_text = "What is the name of this song?"

    if len(options) > 3:
        # we take all answers different than our correct one and then reach for just 3 of them
        incorrect_options = [answer for answer in options if answer != correct_answer]
        incorrect_options = random.sample(incorrect_options, 3)

        # we get those 4 possible options for our quiz and we shuffle them
        options = incorrect_options + [correct_answer]
        random.shuffle(options)

    # saving currect track in cookies to check it later
    session["current_track"] = current_track

    # removing currently played track from list to avoid repetitions
    tracks.remove(current_track)
    cache.set(playlist_uuid, tracks)

    # we return a dictionary containing all important data
    return {
        "track": current_track,
        "options": options,
        "question_text": question_text,
    }


@app.route('/quiz_page', methods=['GET', 'POST'])
def quiz_page():
    if not session.get("playlist_uuid"):
        return redirect("/")

    if request.method == "GET":
        if session["track_count"] == 0:
            score = session.get("score")
            total_questions = session.get("total_questions")
            session.clear()
            return render_template("final.html",
                                   score=score,
                                   total_questions=total_questions)

        # we use our helper function to get all data (quiz question, answers, track)
        data = get_quiz_question()

        # if we get nothing back then something went wrong, we redirect user to index page
        if not data:
            return redirect("/")

        return render_template("quiz.html",
                               track=data['track'],
                               options=data['options'],
                               question_text=data['question_text'],
                               round_duration=session.get('round_duration'))
    else:
        # getting answers to check their values
        user_answer = request.form.get("answer")
        current_track = session.get("current_track")

        # decreasing rounds left
        session["track_count"] = session.get("track_count") - 1

        is_correct = False

        # updating points if the value is correct
        if user_answer == current_track['artist'] or user_answer == current_track['name']:
            session["score"] = session.get("score") + 1
            is_correct = True

        return render_template("check.html",
                               is_correct=is_correct,
                               current_score=session.get("score"),
                               remaining_rounds=session.get("track_count"),
                               current_track_name=current_track['name'],
                               current_track_artist=current_track['artist'])
