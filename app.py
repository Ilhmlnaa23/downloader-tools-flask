from flask import Flask, request, send_file, jsonify, abort
from engine import *
import os
from functools import wraps
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import shutil

app = Flask(__name__,)
app.secret_key = "garox"
app.config['UPLOAD_FOLDER'] = 'media/youtube'
app.config['SESSION_TYPE'] = 'filesystem'

linksource = 'source_url'

@app.route('/')
def index():
    response_data = {"Status": 'Ready'}
    return response_data

# AUTH KE API ENDPOINT
VALID_API_KEYS = ["theworldinyourhand", "myapixaas"]

def validate_api_key(api_key):
    return api_key in VALID_API_KEYS

def api_key_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("Api-Key")

        if not api_key or not validate_api_key(api_key):
            abort(401, description="Unauthorized: Invalid API key.")

        return func(*args, **kwargs)

    return decorated_function


class sosial_downloader:
# Youtube Downloader Start
    @app.route('/youtube_downloader', methods=['GET', 'POST'])
    @api_key_required
    def youtube_downloader_page():
        new_file = None

        if request.method == 'POST':
            video_url = request.form[linksource]
            title = youtube_title(video_url)

            download_option = request.form.get('download_option')
            download_mp3 = download_option == "audio"
            download_mp4 = download_option == "video"

            if download_mp3:
                title += ".mp3"
                title, new_file = download_audio_yt(video_url, os.path.join(app.config['UPLOAD_FOLDER'], title))
            elif download_mp4:
                title += ".mp4"
                title, new_file = download_video_yt(video_url, os.path.join(app.config['UPLOAD_FOLDER'], title))

        if new_file is not None:
            url = f"/downloaded_youtube/{os.path.basename(new_file)}"
            response_data = {
                "name": os.path.basename(new_file),
                "success": True,
                "url": url
            }
        else:
            response_data = {
                "success": False,
                "error": "Failed to download the file."
            }

        return jsonify(response_data)

    @app.route('/downloaded_youtube/<new_file>')
    def download_youtube_file(new_file):
        media_folder = os.path.join("media/youtube")
        file_path = os.path.join(media_folder, new_file)
        return send_file(file_path, as_attachment=True)

# Youtube Downloader End

# Twitter Downloader Start
    @app.route('/twitter_downloader', methods=['POST', 'GET'])
    @api_key_required
    def twitter_downloader():
        if request.method == 'POST':
            url = request.form[linksource]
            option = request.form['download_option'] 

            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com"
            }

            query_params = {
                "url": url
            }

            try:
                response = requests.get(TWITTER_API_URL, headers=headers, params=query_params)
                data = response.json()

                description = data.get("description")

                if option == "image":
                    media = data.get("media", {})
                    photos = media.get("photo", [0])
                    photo_proses = [photo.get("url") for photo in photos]
                    photo_url = photo_proses[0] if photo_proses else None
                    # hasil_download = [{"name": description, "url": photo_url}]
                    response_data = {
                        "success": True,
                        "url": photo_url,
                        "title": description
                    }

                elif option == "video":
                    media = data.get("media", {})
                    video = media.get("video", {})
                    video_variants = video.get("videoVariants", [])
                    url = video_variants[0].get("url")  # Mengambil URL video pertama
                    response_data = {
                        "success": True,
                        "url": url
            }
                else:
                    url = None
                    response_data = {
                        "success": False,
                        "error": "Failed to download the file."
            }


                
                return jsonify(response_data)
            
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}"

 # Twitter Downloader End

# Instagram Downloader Start
    @app.route('/instagram_downloader', methods=['POST'])
    @api_key_required
    def instagram_downloader():
        url = request.form[linksource]
        file_name = None  # 
        #timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")

        download_option = request.form.get('download_option')
        if download_option == "image":
            formatted_date = download_post_ig(url)  
            file_name = formatted_date + ".jpg"
        elif download_option == "video":
            formatted_date = download_post_ig(url)  
            file_name = formatted_date + ".mp4"

        url = f"/downloaded_instagram/{file_name}"
        hasil_download = [{"url": url, "name": file_name}]

        if file_name is not None:
            response_data = {
                "success": True,
                "title": file_name,
                "url": url
            }

        else:
            response_data = {
                "success": False,
                "error": "Failed to download the file."
            }
        
        return jsonify(response_data)
 

    @app.route('/downloaded_instagram/<file_name>')
    def download_instagram_file(file_name):
        media_folder = os.path.join("media","instagram")
        file_path = os.path.join(media_folder, file_name)
        return send_file(file_path, as_attachment=True)

# Instagram Downloader End

# Tiktok Downloader Start
    @app.route('/tiktok_downloader', methods=['POST', 'GET'])
    @api_key_required
    def tiktok_downloader_page():
        if request.method == 'POST':
            url = request.form[linksource]
            option = request.form['download_option']  # This should be either "audio" or "video"
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
            }

            query_params = {
                "url": url
            }

            try:
                response = requests.get(TIKTOK_API_URL, headers=headers, params=query_params)
                data = response.json()

                if option == "audio":
                    audio_url = data.get("data", {}).get("music")
                    audio_title = data.get("data", {}).get("title")
                    url = audio_url
                    response_data = {
                        "success": True,
                        "url": url
                    }

                elif option == "video":
                    video_url = data.get("data", {}).get("play")
                    video_title = data.get("data", {}).get("title")
                    url = video_url
                    response_data = {
                        "success": True,
                        "url": url
                    }
                    
                return jsonify(response_data)
            except requests.exceptions.RequestException as e:
                response_data = {
                    "success": False,
                    "error": "Failed to download the file."
                }
                

            

    @app.route('/downloaded_tiktok/<file_name>')
    def download_tiktok_file(file_name):
        media_folder = os.path.join("media", "tiktok")
        file_path = os.path.join(media_folder, file_name)
        return send_file(file_path, as_attachment=True)

# Tiktok Downloader End

# Spotify Downloader Start
    @app.route('/spotify_downloader', methods=['POST'])
    def spotify_downloader_page():
        if request.method == 'POST':
            song_url = request.form[linksource]
            output_folder = os.path.join("media/spotify")

            try:
                title = download_song_from_spotify(song_url, output_folder)
                file_name = f"{title}.mp3"
                url = f"/downloaded_spotify/{file_name}"
                response_data = {
                        "success": True,
                        "title": file_name,
                        "url": url
                    }
            except Exception as e:
                response_data = {
                        "success": True,
                        "title": file_name,
                        "url": url
                    }

            return jsonify(response_data)

    
    @app.route('/downloaded_spotify/<file_name>')
    def download_spotify_file(file_name):
        media_folder = os.path.join("media", "spotify")
        file_path = os.path.join(media_folder, file_name)
        return send_file(file_path, as_attachment=True)

# Spotify Downloader End

# Fungsi untuk menghapus folder
def delete_folders_contents():
    media_folder = os.path.join("media")
    def delete_contents_windows(path):
        os.system(f"rd /s /q \"{path}\"")
    def delete_contents_linux(path):
        shutil.rmtree(path)
    if os.path.exists(media_folder):
        if os.name == "nt":  # Windows
            delete_contents_windows(media_folder)
        else:  # Linux 
                delete_contents_linux(media_folder)
    print("Downloader Media Folder Clear")

    # Schedule the deletion job to run every hour
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_folders_contents, 'interval', hours=2)
    scheduler.start()

# ...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080, debug=True)

# ...
