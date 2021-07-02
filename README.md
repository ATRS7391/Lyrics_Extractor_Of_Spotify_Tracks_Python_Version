
# Lyrics Extractor Of Spotify Tracks
## `.py` Version, for Python users

A program/tool written in Python that extract the lyrics of a Spotify track using web scraping. Then saves it into `.txt` file inside `Lyrics` folder. It can also extract lyrics of all the tracks in a Spotify playlist.






## Instructions

1. Make a new folder named `Lyrics` in the same directory of `LyricsExtractor.py`.
2. Make a new `Genius API-Client` by clicking [here](https://genius.com/api-clients/new). Login if required. Copy the `Client Secret` and then paste it in `API_Credentials.json` in the correct key value place.
3. Make a new `Spotify API-Application` by clicking [here](https://developer.spotify.com/dashboard/applications). Login if required. Then click on `CREATE AN APP`. Copy `Client ID` and `Client Secret` and then paste it in their respective values in `API_Credentials.json`.
4. Now install the required packages using `pip install Requirements.txt` in Powershell/Command Prompt opened in the same directory of `Requirements.txt`.
5. Now fire up your `Spotify` then copy the URL of the track or playlist you want to get lyrics.
6. Open the main program i.e. `LyricsExtractor.py` and then put the URL of the track/playlist when asked to. After that if the `API Credentials` and `Spotify URL` are correct, the program will start to extract lyrics and saves them into `Lyrics` folder.
    
## Features

- Can extract and save lyrics of a single track
- Can extract and save lyrics of the tracks of a full playlist

  
## Requirements

#### Programs:
- Python 3 and above
#### Packages:
- certifi
- requests
- spotipy
- urllib3
- bs4

  
## About

- Creator: ATRS
- Created On: 29-06-2021
- Version: 1.0
- Language: Python 3.9
  
## License

[MIT](https://github.com/ATRS7391/Lyrics_Extractor_Of_Spotify_Tracks_Python_Version/blob/main/LICENSE)

  
### Note: For educational purposes only

  
