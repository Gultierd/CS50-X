# Music Quiz for cs50!
#### Description:
## MUSIC QUIZ APP!
Following project is a web-based music quiz app built with Python and using Flask framework to stitch it all together.
Users can play the quiz just by entering a Deezer's playlist URL, from which the app uses Deezer's API to reach the data inside.
Designed to be both interactive and user-friendly, coated with Dark and yellow color palette.

## Project files:
The core of the application is app.py file, handling all the server-side logic and entire routing. It contains following routes:
### "/"
Homepage where user enters a Deezer playlist URL. It also serves as the main entry point to restart the quiz, clearing any previous session data.
### "/quiz"
Processes the URL and validates it, fetches back the necessary track data from Deezer API. Stores data in server-side cache and redirects user further to settings page
### "/settings"
After getting data from Deezer API the user can customize their quiz experience, by choosing number of tracks in quiz (with a given maximum),
round duration (up to 30 seconds given Deezer's API limitations) and question types (both artist and title questions)
### "/quiz_page"
Main quiz interface. Handles "GET" requests to display new questions using a helper method get_quiz_question and "POST" requests to process user answers. Keeps track of user's score and remaining rounds

##  HTML Templates:
Music Quiz uses several HTML files to render the user interface, all of which styled with Boostrap 5 for fitting and matching design for pages:
### index.html
Landing page where users input a Deezer playlist URL
### settings.html
Page where user can configure quiz parameters before the game begins, offering early client-sided data validation before sending to server.
Displays the playlist's cover art and title from Deezer web page.
### quiz.html
Main quiz page, playing the music from Deezer API in the background, featuring the question with multiple choice options.
It also contains a simple Javascript countdown timer to keep the game interesting.
### check.html
Feedback page displayed after each question, Showing results of each question, current score and remaining rounds in the game
### final.html
Page that marks the end of the quiz. Displays user's final score and enables the users to play again

## Design Choices:
While many design choices and practices were taken straight from the cs50x course, several of them were made in a differrent manner,
allowing for a great learning experience.
### Session and Cache:
One of the issues faced during the development was handling the data transfer between pages.
Initially all data was stored directly in Flask session, but was quickly identified as a problem, because of its large size
some browsers use a size limit around 4kb and many larger playlists would exceed this limit.
Solving this was rather simple - creation of additional server-sided cache in order to store the full list of tracks for current playlist.
Then for that playlist we store a unique identifier (UUID) in user's session, by which we can reach the data inside.
This approach allows the application to handle larger playlists without any data size constraints on client side.
### API selection:
 The first issue that appeared during development was choosing the data source for our quiz playlists.
 Both Spotify and Youtube Music APIs required the user to log in and also handled the entire logic around access tokens.
 This appeared as a great obstacle, as users would have a much rougher experience.
 Deezer does not require the user to provide any data, offers a wide selection of songs that contribute to seamless experience for users.
