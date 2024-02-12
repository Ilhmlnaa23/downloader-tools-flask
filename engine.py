import os
import os
import re
import sys
import time
import json
import requests
import pyfiglet
import instaloader
from tqdm import tqdm
from pytube import YouTube
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore
from datetime import datetime
from datetime import datetime, timezone, timedelta
import json
import random
import string
import subprocess
import mysql.connector
import shortuuid
# Fungsi untuk mengatur ukuran lebar layar terminal
def set_terminal_width(columns):
    os.system(f"mode con: cols={columns}")

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Fungsi untuk menampilkan pesan teks dan meminta input dari pengguna
def input_with_prompt(prompt):
    return input(prompt)


###################YOUTUBE DOWNLOADER###########################
def youtube_title(url):
    try:
        youtube = YouTube(url, on_progress_callback=progress_function)
        video_title = youtube.title
        print("Video Title:", video_title)
        return video_title
    except Exception as e:
        print("Error:", str(e))
        return None

def download_video_yt(url, output_path=None):
    new_file = None
    try:
        # Membuat objek YouTube
        #youtube = YouTube(url)
        youtube = YouTube(url, on_progress_callback=progress_function)
        # Menampilkan informasi tentang video
        # print(f"{Fore.CYAN}Judul video:", youtube.title)
        # print(f"{Fore.CYAN}Durasi video:", youtube.length, "detik")
        # print()
        # Memilih stream dengan kualitas tertinggi
        video_stream = youtube.streams.get_highest_resolution()

        # Memulai proses pengunduhan
        print(f"{Fore.BLUE}Memulai pengunduhan video...")
        
        output_file = video_stream.download(output_path=os.path.join("media", "youtube"))
        video_title = youtube.title
        # Mengubah ekstensi file menjadi MP3
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp4'
        os.rename(output_file, new_file)
        
        print(f"{Fore.GREEN}Pengunduhan video berhasil!")
    except Exception as e:
        print(f"{Fore.RED}Terjadi kesalahan saat mengunduh video:", str(e))
    return youtube.title, new_file


def download_audio_yt(url, output_path=None):
    new_file = None
    try:
        # Membuat objek YouTube
        #youtube = YouTube(url)
        youtube = YouTube(url, on_progress_callback=progress_function)
        # Menampilkan informasi tentang video
        # print(f"{Fore.CYAN}Judul video:", youtube.title)
        # print(f"{Fore.CYAN}Durasi video:", youtube.length, "detik")
        # print()
        #print("Nama Channel:", youtube.channel_id)
        # Memilih stream dengan format audio (audio-only)
        audio_stream = youtube.streams.filter(only_audio=True).first()

        output_file = audio_stream.download(output_path=os.path.join("media", "youtube"))
        video_title = youtube.title
        # Mengubah ekstensi file menjadi MP3
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)

        print(f"{Fore.GREEN}Pengunduhan audio berhasil!")
    except Exception as e:
        print(f"{Fore.RED}Terjadi kesalahan saat mengunduh audio:", str(e))
    return youtube.title, new_file
   

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size / 1024) / 1024
    totalsz = round(totalsz, 1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion, 2)

    # Karakter animasi untuk membuat efek bergerak
    animation_chars = ".oO0"

    # Menghitung jumlah karakter animasi berdasarkan persentase yang didapat
    animated_chars_count = int(percentage_of_completion / 100 * len(animation_chars))
    animated_chars = animation_chars[:animated_chars_count]

    # Menggunakan tqdm.write untuk mencetak status tanpa newline
    tqdm.write(
        f'{Fore.GREEN}Download Progress: {percentage_of_completion:.2f}%, Total Size: {totalsz} MB, Downloaded: {dwnd} MB, Remaining: {remain} MB {animated_chars}',
        end='\r'
    )


###################PINTEREST DOWNLOADER###########################
def download_file(url, filename):
    response = requests.get(url, stream=True)

    file_size = int(response.headers.get('Content-Length', 0))
    progress = tqdm(response.iter_content(1024), f'Downloading {filename}', total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

    with open(filename, 'wb') as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    progress.close()

def pinterest_image_downloader(page_url):
    if "pinterest.com/pin/" not in page_url and "https://pin.it/" not in page_url:
        print(f"{Fore.RED}URL yang dimasukan tidak valid")
        return

    if "https://pin.it/" in page_url:  # Pin URL short check
        print(f"{Fore.RED}Extract original pin link")
        t_body = requests.get(page_url)
        if t_body.status_code != 200:
            print(f"{Fore.RED}URL yang dimasukan tidak valid atau tidak berfungsi.")
            return
        soup = BeautifulSoup(t_body.content, "html.parser")
        href_link = (soup.find("link", rel="alternate"))['href']
        match = re.search('url=(.*?)&', href_link)
        page_url = match.group(1)  # Update page URL

    print(f"{Fore.RED}Mengecek Gambar dari URL yang diberikan")
    body = requests.get(page_url)  # GET response from URL
    if body.status_code != 200:  # Check status code
        print(f"{Fore.RED}URL yang dimasukan tidak valid atau tidak berfungsi.")
        return

    soup = BeautifulSoup(body.content, "html.parser")  # Parse the content

    print(f"{Fore.RED}Gambar Terdeteksi.")
    print(f"{Fore.BLUE}Proses Download...")
    # Extracting the URL
    image_element = soup.find("img", class_="hCL kVc L4E MIw")
    if not image_element:
        print(f"{Fore.RED}Tidak ada gambar di halaman ini.")
        return

    extract_url = image_element['src']

    output_folder = os.path.join("media", "pinterest")
    os.makedirs(output_folder, exist_ok=True)
    file_name = datetime.now().strftime("%d_%m_%H_%M_%S_") + ".png"
    output_path = os.path.join(output_folder, file_name)
    download_file(extract_url, output_path)
    
    print(f"{Fore.GREEN}Gambar Berhasil Di Download:", file_name)
    return output_path

def pinterest_video_downloader(page_url):
    if("pinterest.com/pin/" not in page_url and "https://pin.it/" not in page_url):
        print(f"{Fore.RED}URL yang dimasukan tidak valid")
        exit()

    if("https://pin.it/" in page_url): # pin url short check
        print("extracting orignal pin link")
        t_body = requests.get(page_url)
        if(t_body.status_code != 200):
            print(f"{Fore.RED}URL yang dimasukan tidak valid atau tidak berfungsi.")
            return
        soup = BeautifulSoup(t_body.content,"html.parser")
        href_link = (soup.find("link",rel="alternate"))['href']
        match = re.search('url=(.*?)&', href_link)
        page_url = match.group(1) # update page url 

    print(f"{Fore.RED}Mengecek Video dari URL yang diberikan")
    body = requests.get(page_url) # GET response from url
    if(body.status_code != 200): # checks status code
        print(f"{Fore.RED}URL yang dimasukan tidak valid atau tidak berfungsi.")
    else:
        soup = BeautifulSoup(body.content, "html.parser") # parsing the content
        ''' extracting the url
        <video
            autoplay="" class="hwa kVc MIw L4E"
            src="https://v1.pinimg.com/videos/mc/hls/......m3u8"
            ....
        ></video>
        '''
    
    print(f"{Fore.RED}Video Terdeteksi")
    print(f"{Fore.BLUE}Proses Download...")
    # Extracting the URL
    video_element = soup.find("video", class_="hwa kVc MIw L4E")
    if not video_element:
        print(f"{Fore.RED}Tidak ada video di halaman ini.")
        return

    extract_url = (soup.find("video",class_="hwa kVc MIw L4E"))['src'] 
    convert_url = extract_url.replace("hls","720p").replace("m3u8","mp4")

    output_folder = os.path.join("media", "pinterest")
    os.makedirs(output_folder, exist_ok=True)
    file_name = datetime.now().strftime("%d_%m_%H_%M_%S_") + ".mp4"
    output_path = os.path.join(output_folder, file_name)
    download_file(convert_url, output_path)

    print(f"{Fore.GREEN}Video Berhasil Di Download:", file_name)
    return output_path

#MENU PINTEREST
def get_Pinterest_api_status():
    api_url = "https://pin.it"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return "ONLINE"
        else:
            return "OFFLINE"
    except requests.exceptions.RequestException:
        return "OFFLINE"

###################TWITTER VIDIO DOWNLOADER############################
def extract_video_id(url) -> None | int:
    pattern = r"status/(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def download_video(url, file_path) -> None:
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open(file_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    print()
    print(f"{Fore.YELLOW}Vidio Berhasil Di Download! Saved to: {file_path}")


def download_twitter_video(url, file_name):
    video_id = extract_video_id(url)
    api_url = f"https://api.twitterpicker.com/tweet/mediav2?id={video_id}"

    response = requests.get(api_url)
    data = response.json()

    videos = data["media"]["videos"][0]["variants"]
    highest_bitrate = max(videos, key=lambda x: int(x.get("bitrate", 0) or 0))
    video_url = highest_bitrate["url"]

    save_folder = os.path.join("media", "twitter")
    os.makedirs(save_folder, exist_ok=True)  
    file_path = os.path.join(save_folder, file_name)  

    download_video(video_url, file_path)

###################TWITTER IMAGES DOWNLOADER############################
def extract_images_id(url) -> None | int:
    pattern = r"status/(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def download_images(url, file_path) -> None:
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open(file_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    print()
    print(f"{Fore.YELLOW}Gambar Berhasil Di Download! Saved to: {file_path}")


def download_twitter_images(url, file_name):
    images_id = extract_images_id(url)
    api_url = f"https://api.twitterpicker.com/tweet/mediav2?id={images_id}"
    print(images_id)

    response = requests.get(api_url)
    data = response.json()

    images = data["media"]["thumbnail"][0]["variants"]
    highest_bitrate = max(images, key=lambda x: int(x.get("bitrate", 0) or 0))
    images_url = highest_bitrate["url"]

    save_folder = os.path.join("media", "twitter")
    os.makedirs(save_folder, exist_ok=True)  
    file_path = os.path.join(save_folder, file_name)  

    download_images(images_url, file_path)


##MYSCRIP-MENU-TWITTER##
def get_twitter_api_status():
    api_url = "https://rapidapi.com"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return "ONLINE"
        else:
            return "OFFLINE"
    except requests.exceptions.RequestException:
        return "OFFLINE"

###################INSTAGRAM DOWNLOADER##########################

# Fungsi untuk mendownload media dari URL Instagram
def download_post_ig(url):
    try:
        insta = instaloader.Instaloader(dirname_pattern='media/instagram')
        post = instaloader.Post.from_shortcode(insta.context, url.split("/")[-2])

        post_date = post.date
        formatted_date = post_date.strftime("%Y-%m-%d_%H-%M-%S_UTC")
        output_folder = os.path.join("media", "instagram")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder)

        insta.download_post(post, target=output_path)

        # Count the number of images downloaded
        image_count = sum(1 for file in os.listdir(output_path) if formatted_date in file and file.endswith('.jpg'))
        video_count = sum(1 for file in os.listdir(output_path) if formatted_date in file and file.endswith('.mp4'))

        if image_count > 1 :
            formatted_date = post_date.strftime("%Y-%m-%d_%H-%M-%S_UTC")


        return formatted_date, image_count, video_count
    except instaloader.exceptions.InstaloaderException as e:
        print("Terjadi kesalahan saat mengunduh media:", str(e))
    except Exception as e:
        print("Terjadi kesalahan:", str(e))


###################TIKTOK DOWNLOADER##########################

def download_tiktok_file(url, file_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    with open(file_path, "wb") as file:
        for data in response.iter_content(block_size):
            file.write(data)

def download_tiktok_video(url, file_name):
    api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "f1a58d4d97msh22d8e0597709c97p136e8bjsn8083accf3f5f",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    params = {
        "url": url,
        "hd": "1"
    }
    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()

        video_url = data.get("data", {}).get("play")
        video_title = data.get("data", {}).get("title")

        if not video_url:
            print("Failed to get video URL.")
            return

        output_folder = os.path.join("media", "tiktok")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, file_name)

        print(f"Downloading TikTok video: {video_title}")
        download_tiktok_file(video_url, output_path)

        print("TikTok video download completed!")
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

def download_tiktok_audio(url, file_name):
    api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "f1a58d4d97msh22d8e0597709c97p136e8bjsn8083accf3f5f",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    params = {
        "url": url,
        "hd": "1"
    }
    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()

        audio_url = data.get("data", {}).get("music")
        audio_title = data.get("data", {}).get("title")

        if not audio_url:
            print("Failed to get audio URL.")
            return

        output_folder = os.path.join("media", "tiktok")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, file_name)

        print(f"Downloading TikTok audio: {audio_title}")
        download_tiktok_file(audio_url, output_path)

        print("TikTok audio download completed!")
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


def get_current_date_string():
    return datetime.now().strftime("%d_%m_%Y_%H")

def generate_random_code(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def get_tiktok_api_status():
    api_url = "https://rapidapi.com"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return "ONLINE"
        else:
            return "OFFLINE"
    except requests.exceptions.RequestException:
        return "OFFLINE"
    

###################SPOTIFY DOWNLOADER##########################
def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def download_song_from_spotify(song_url, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        os.chdir(output_folder)  # Mengubah direktori kerja
        random_filename = f"{generate_random_string()}.spotdl"
        command = f"spotdl {song_url} --save-file {random_filename}"
        subprocess.run(command, shell=True, check=True)
       
        # Membaca file .spotdl yang berisi metadata (format JSON)
        metadata_filename = random_filename  # Nama file sama dengan yang digenerate secara random
        with open(metadata_filename) as json_file:
            data = json.load(json_file)
            title = data[0].get('name', 'Unknown')
            artist = ', '.join(data[0].get('artists', ['Unknown']))
        judul = artist + ' - ' + title
        print("Lagu berhasil diunduh!")
        print(judul)
        os.remove(random_filename)  # Menghapus file .spotdl setelah selesai
        return judul
    except subprocess.CalledProcessError as e:
        print("Terjadi kesalahan saat mengunduh lagu:", str(e))
        return None
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
        return None
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_spotify_api_status():
    api_url = "https://rapidapi.com"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return "ONLINE"
        else:
            return "OFFLINE"
    except requests.exceptions.RequestException:
        return "OFFLINE"

SPOTIFY_API_URL = "https://spotify-downloader3.p.rapidapi.com/spotify/download/"
TWITTER_API_URL = "https://twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com/status"
TIKTOK_API_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
RAPIDAPI_KEY = "f1a58d4d97msh22d8e0597709c97p136e8bjsn8083accf3f5f"



###################FITUR URL SHORTENER##########################
# db_connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="url_shortener"
# )

# # Fungsi untuk memeriksa apakah custom URL sudah ada dalam database
# def is_custom_url_taken(short_id):
#     cursor = db_connection.cursor()
#     cursor.execute("SELECT COUNT(*) FROM urls WHERE short_id = %s", (short_id,))
#     count = cursor.fetchone()[0]
#     cursor.close()
#     return count > 0

# def generate_short_id():
#     return shortuuid.uuid()[:5]



def check_engine_status():
    engine_file = 'engine.py'
    if os.path.exists(engine_file):
        return 'ONLINE'
    else:
        return 'OFFLINE'