from flask import Flask, request, url_for, redirect, render_template
import spotipy, os, json
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius as genius

print('Python Launched...')
os.chdir(os.path.abspath(r'C:\Users\diego\Documents\My Stuff\Programming Stuff\web project'))

def creds():
    global spotify

    redirect_uri = 'https://google.com/'
    client_id = '11487a86ac44499da9a054bb54d09dee'
    client_secret = 'eebbb8c95fb149058021a7dd7e148ffd'
    scope = 'user-read-currently-playing user-library-read'
    username = 'prtg0pf13wo9ik7a9ra2h31fa'

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,
                                   redirect_uri=redirect_uri) # 'localhost:8080' also works as a redirect uri
    # except: # there was a try block above, with the thing indented
    #     os.remove(f".cache-{username}")

    spotify = spotipy.Spotify(auth=token)

def getlyrics():

    print('\nSearching...')
    currenttrack = spotify.current_user_playing_track()

    searcher1 = currenttrack['item'] # narrows it down to all the useful stuff
    artist = searcher1['artists'][0]['name'] # gets key, the list is just one dictionary so takes the dictionary out of the list, gets string
    album = searcher1['album']['name'] # finds the album
    track = searcher1['name']
    ider = searcher1['id']   # this is the spotify code for the song, it is its own entry in the main dict

    global headinfo
    headinfo = f'''
Artist -  {artist}
Track  -  {track}
Album  -  {album}

'''

    #↓ this changes 'The Weeknd' to 'Weeknd, The'
    def thethefixer(inputer=artist):
        global artistfilename
        if (inputer[0:3] == 'The') == True:
            inputer = inputer[4:] + ', The'
        artistfilename = inputer
    thethefixer()

    queryer = artist + ' - ' + track # this is the thing i am searching genius for
    badcharachterlist = ['?', '/', '\\', '|']
    for x in badcharachterlist:
        queryer = queryer.replace(x, '') # these charachters dont work in links or file names

    #genius thingy
    api = genius.Genius('S2hTR51IMeB7MePXMZJE7Upz-uMj0Rmb6wtBvd3k2tp5-ehj6r7KZXk2e0L-F9fY')
    lyrics = api.search_song(queryer)
    lyrics.save_lyrics('lyricer.json')

    with open('lyricer.json', 'r') as file:
        jsonfilelist = json.load(file)
        global stringvar
        stringvar = str(jsonfilelist["lyrics"])
        #print(stringvar)

    try:
        os.remove('lyricer.json')
    except:
        None

    return headinfo
    return stringvar

app = Flask(__name__)

@app.route("/")
def index():
    creds()
    getlyrics()
    return render_template('index.html', headinfo=headinfo, lyrics=stringvar)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for(index))
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

