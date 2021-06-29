import json
import re
import subprocess
import sys
import urllib.error
import urllib.request


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


try:
    import certifi
except:
    print("Installing required Modules... Only for first time... ")
    pip_install("certifi")
    import certifi

try:
    import requests
except:
    print("Installing required Modules... Only for first time... ")
    pip_install("requests")
    import requests

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except:
    print("Installing required Modules... Only for first time... ")
    pip_install("spotipy")
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

try:
    import urllib3
except:
    print("Installing required Modules... Only for first time... ")
    pip_install("urllib3")
    import urllib3

try:
    from bs4 import BeautifulSoup
except:
    print("Installing required Modules... Only for first time... ")
    pip_install("bs4")
    from bs4 import BeautifulSoup


class GetLyrics:
    def __init__(self):
        self.title = None
        self.artist = None
        self.lyrics = None
        self.source = None
        self.query = None
        self.api_key = None
        self.url = None

    def google_lyrics(self, query):
        query = str(query)
        try:
            url = "https://www.google.com/search?q=" + query.replace(" ", "+") + "+lyrics"

            r = requests.get(url)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent, "html.parser")

            title = str(html_content.find("span", class_="BNeawe tAd8D AP7Wnd"))
            title = re.sub(r"(<.*?>)*", "", title).replace("[", "").replace("]", "")

            artist = html_content.find_all("span", class_="BNeawe s3v9rd AP7Wnd")
            artist = str(artist[1])
            artist = re.sub(r"(<.*?>)*", "", artist).replace("[", "").replace("]", "")

            lyrics = html_content.find_all("div", class_="BNeawe tAd8D AP7Wnd")
            lyrics = str(lyrics[2])
            lyrics = re.sub(r"(<.*?>)*", "", lyrics).replace("[", "").replace("]", "")

            source = str(html_content.find("span", class_="uEec3 AP7Wnd"))
            source = re.sub(r"(<.*?>)*", "", source).replace("[", "").replace("]", "")

            if lyrics is None or artist is None or title is None or source is None:
                raise Exception("Something went wrong. No lyrics yielded. ")

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = source  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = None  # API Key provided by the user (Here not required)
            self.url = None
        except:
            raise Exception

    def genius_lyrics(self, query, api_key):
        query = str(query)
        api_key = str(api_key)
        try:
            url = "https://api.genius.com/search?access_token=" + api_key + "&q=" + query.replace("&",
                                                                                                  "and").replace(
                "by", "-").replace(" ", "%20")
            details = urllib.request.urlopen(url).read().decode()
            json_results = json.loads(details)

            title = str(json_results["response"]["hits"][0]["result"]["title"])
            artist = str(json_results["response"]["hits"][0]["result"]["primary_artist"]["name"])
            genius_url = str(json_results["response"]["hits"][0]["result"]["url"])
            url1 = genius_url
            r = requests.get(url1)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent.decode("utf-8").replace("<br/>", "\n"), "html.parser")

            lyrics = str(html_content.find("div", class_=re.compile("^lyrics$|Lyrics__Root")).get_text())
            lyrics = re.sub(r"(\[.*?])*", "", lyrics).strip()
            lyrics = lyrics.replace("EmbedShare Url:CopyEmbed:Copy", "").strip()
            lyrics = re.sub('\n\n+', '\n\n', lyrics)

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Genius"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = api_key  # API Key provided by the user
            self.url = url1
        except:
            raise Exception

    def musixmatch_lyrics(self, query):
        query = str(query)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)      Chrome/74.0.3729.169 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
            url = 'https://www.musixmatch.com/search/' + query.replace(" ", "%20")  # +'/lyrics'
            http = urllib3.PoolManager(ca_certs=certifi.where())
            resp = http.request('GET', url, headers=headers)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")
            href = str(html_content.find("a", class_="title")).split("href=")[1].split('''"''')[1]
            new_link = "https://www.musixmatch.com/" + href
            http = urllib3.PoolManager(ca_certs=certifi.where())
            url = new_link
            resp = http.request('GET', url, headers=headers)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")

            artist = str(html_content.find("a", class_="mxm-track-title__artist mxm-track-title__artist-link"))
            artist = re.sub(r"(<.*?>)*", "", artist)

            title = str(html_content.find("h1", class_="mxm-track-title__track").getText("//")).split("//")[-1]
            title = re.sub(r"(<.*?>)*", "", title)

            lyrics = html_content.findAll("span", class_="lyrics__content__ok")
            lyrics = str(lyrics[0]) + "\n" + str(lyrics[1])
            lyrics = re.sub(r"(<.*?>)*", "", lyrics)

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Musixmatch"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = None  # API Key provided by the user
            self.url = new_link
        except:
            raise Exception


spotify_client_id = None
spotify_client_secret = None
genius_client_secret = None


def get_lyrics(full_title, genius_client_secret_api):
    query_title = str(full_title)  # .encode('utf-8')
    query_title = re.sub(r'[^\w]', ' ', query_title)
    query_title = re.sub(' +', ' ', query_title)
    ly = GetLyrics()
    try:
        ly.musixmatch_lyrics(query_title)
    except:
        try:
            ly.google_lyrics(query_title)
        except:
            ly.genius_lyrics(query_title, genius_client_secret_api)
    lyrics = f"""
{ly.title}
{ly.artist}
 
--------

{ly.lyrics}


---------------------------------
Lyrics provided by {ly.source}
"""
    return lyrics


# Print Header
header = """

 +--------------------------+
 | Spotify Lyrics Extractor |
 +--------------------------+

    """
print(header)

# Check Internet Connection
host = "http://google.com"
print(" Checking for active internet connection. ")
try:
    urllib.request.urlopen(host)
    print(" [✓] Successful. \n ")
    pass
except urllib.error.URLError:
    print(" [x] No active internet connection detected. Press any key to exit. \n ")
    input()
    exit()

# Get and check Credentials
print(" Getting your API Credentials from 'API_Credentials.json'. ")
try:
    api_credentials = open("API_Credentials.json", "r")
    api_data = json.load(api_credentials)
    spotify_client_id = api_data["API_Credentials"]["Spotify_Client_ID"]
    spotify_client_secret = api_data["API_Credentials"]["Spotify_Client_Secret"]
    genius_client_secret = api_data["API_Credentials"]["Genius_Client_Secret"]

    if spotify_client_id == "None" or spotify_client_secret == "None" or genius_client_secret == "None":
        print(" [x] Any field in 'API_Credentials.json' is empty. Please read "
              "'Instructions.txt' before executing the code. Press any key to exit. \n ")
        input()
        exit()
    else:
        print(" [✓] Successful. \n ")
except KeyError:
    print(" [x] Seems like 'API_Credentials.json''s key values had been changed. Cannot fetch "
          "details. Press any key to exit. \n ")
    input()
    exit()

query_type = None

# Get Query as Link or String
url = input(" Please enter Spotify Playlist URL or Track URL: ")

if url.isspace() or url == "" or url == " ":
    print(" [x] Spotify playlist url is empty. Press any key to exit. \n ")
    input()
    exit()
elif url.strip().startswith("https://open.spotify.com/playlist/"):
    query_type = "Playlist"
    print(" [✓] Successful. \n ")
elif url.strip().startswith("https://open.spotify.com/track/"):
    query_type = "Track"
    print(" [✓] Successful. \n ")
else:
    print(" [x] Invalid Spotify URL. Press any key to exit. \n ")
    input()
    exit()

auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

if query_type is None:
    print(" [x] Some unexpected error occurred. Press any key to exit. \n ")
    input()
    exit()
if query_type == "Playlist":
    songs = []
    print(" Getting all tracks from the Spotify playlist. ")
    playlist_items = None
    try:
        playlist_items = sp.playlist_items(url)
    except:
        print(
            " [x] Something went wrong, make sure you have an active internet connection, url is correct and given API Credentials are valid. Press any key to exit. \n ")
        input()
        quit()
    if playlist_items["total"] == 0:
        print(" [x] Spotify playlist was empty. Press any key to exit. \n ")
        input()
        exit()
    else:
        try:
            tracks = playlist_items['items']
            while playlist_items['next']:
                playlist_items = sp.next(playlist_items)
                tracks.extend(playlist_items['items'])
            songs = []
            for i in tracks:
                artists = []
                for j in i["track"]["artists"]:
                    artists.append(j["name"])
                artists = ", ".join(artists)
                title = i["track"]["name"]
                final_title = artists + " - " + title
                songs.append(final_title)
            print(" [✓] Successful. \n ")
        except:
            print(
                " [x] Something went wrong, make sure you have an active internet connection. Press any key to exit. \n ")
            input()
            exit()
        try:
            c = 0
            t = len(songs)
            for song in songs:
                c += 1
                print(f" Getting lyrics for '{song}' [{c} of {t} songs]")
                try:
                    lyrics = get_lyrics(song, genius_client_secret)
                    f = open(f"Lyrics/{song}.txt", "w+", encoding='utf-8')
                    f.write(lyrics)
                    f.close()
                    print(" [✓] Successful. ")
                except:
                    print(
                        " [x] Can't get lyrics, make sure you have an active internet connection or it might happen that the track only don't have lyrics. \n ")
        except:
            print(
                " [x] Something went wrong, make sure you have an active internet connection. Press any key to exit. \n ")
            input()
            exit()

elif query_type == "Track":
    print(" Getting the track from Spotify. ")
    song = None
    try:
        song = sp.track(url)
        print(" [✓] Successful. \n ")
    except:
        print(
            " [x] Something went wrong, make sure you have an active internet connection, url is correct and given API Credentials are valid. Press any key to exit. ")
        input()
        quit()
    artists = []
    for j in song["artists"]:
        artists.append(j["name"])
    artists = ", ".join(artists)
    title = song["name"]
    final_title = artists + " - " + title
    song = final_title
    print(f" Getting lyrics for '{song}'")
    try:
        lyrics = get_lyrics(song, genius_client_secret)
        f = open(f"Lyrics/{song}.txt", "w+", encoding='utf-8')
        f.write(lyrics)
        f.close()
        print(" [✓] Successful. ")
    except:
        print(
            " [x] Can't get lyrics, make sure you have an active internet connection or it might happen that the track only don't have lyrics. Press any key to exit. \n ")
        input()
        quit()

print(f"\n\n [✓] Successfully all the task is done. Now you can check for the lyrics in 'Lyrics' folder. \n\n ")
