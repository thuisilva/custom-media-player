# i wish for a relationship with as much love as my disgruntlement towards ffmpeg
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import importlib
import sys
import random
import time
import ctypes
import threading
from tempfile import NamedTemporaryFile
os.system("cls" if os.name == "nt" else "clear")

REQUIRED_MODULES = ["googleapiclient", "simpleaudio", "dotenv", "tqdm", "yt_dlp", "moviepy.editor", "pygame", "keyboard", "numpy"]
YOUTUBE_KEY = ""

for module in REQUIRED_MODULES:
    try:
        importlib.import_module(module)
    except ImportError or ModuleNotFoundError:
        print(f"Missing module: {module}")
        choice = input("Would you like to install missing modules? (y/n): ").strip().lower()
        if choice == "y":
            os.system("pip install -r requirements.txt")
            break
        else:
            i=input("Do you want to exit y/n > ").lower()
            if i == "y":
                sys.exit("Please install the required modules and try again.")
            elif i == "n":
                print("Continuing without installing modules may lead to errors.")
            else:
                sys.exit("Invalid input. Exiting program.")

from googleapiclient.discovery import build as google_build
import simpleaudio as sa
import dotenv as denv
import tqdm
import yt_dlp
from moviepy.editor import AudioFileClip, VideoFileClip
import pygame
import keyboard
import numpy as np

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
GetConsoleWindow = kernel32.GetConsoleWindow
GetForegroundWindow = user32.GetForegroundWindow
GetWindowTextW = user32.GetWindowTextW
GetWindowTextLengthW = user32.GetWindowTextLengthW
SetConsoleTitleW = kernel32.SetConsoleTitleW

# Create a unique title (change if you run multiple instances)
unique_title = f"CustomMediaPlayer_{os.getpid()}"

SetConsoleTitleW(unique_title)

def hwnd_title(hwnd):
    if not hwnd:
        return ""
    length = GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def is_console_focused():
    hwnd_fore = GetForegroundWindow()
    return hwnd_title(hwnd_fore) == unique_title

print("All modules imported successfully.")

flogin = None

if os.path.exists(f"data/{os.getlogin()}.txt"):
    with open(f"data/{os.getlogin()}.txt", "r") as configfile:
        lines = configfile.readlines()
        flogin = lines[0].strip()
else:
    with open(f"data/{os.getlogin()}.txt", "w") as configfile:
        configfile.write("False")

if flogin == "False":
    with open(".env", "w") as envfile:
        envfile.write("YOUTUBE_KEY=")
        print("Please set your YOUTUBE_KEY in the .env file created. Refer to the README for setup instructions.")
        input("Press Enter after updating the .env file...")
        try:
            denv.load_dotenv()
            YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")
            if not YOUTUBE_KEY:
                raise ValueError("YOUTUBE_KEY not set.")
        except ValueError as e:
            sys.exit(f"Error loading YOUTUBE_KEY: {e}")
        else:
            with open(f"data/{os.getlogin()}.txt", "w") as configfile:
                configfile.write("True")
elif flogin == "True":
    denv.load_dotenv()
    YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")


yAPI = google_build("youtube", "v3", developerKey=YOUTUBE_KEY)
print("YouTube API client initialized successfully.")
print("================================")

isplaying = False

def convert(playlist_id, single, single_video_id):
    if single != True:
        title = yAPI.playlists().list(part="snippet,contentDetails",id=playlist_id).execute()["items"][0]["snippet"]["title"]
        for file in os.listdir(f"data/playlists/{title}/"):
            if file.endswith(".mp4") or file.endswith(".webm"):
                input_path = f"data/playlists/{title}/{file}"
                output_path = f"data/playlists/{title}/{os.path.splitext(file)[0]}.mp3"
                AudioFileClip(input_path).write_audiofile(output_path, codec="mp3", verbose=False, logger=None)
                os.remove(input_path)
        print(f"Conversion to mp3 completed successfully.")
    else:
        title = yAPI.videos().list(part="snippet,contentDetails",id=single_video_id).execute()["items"][0]["snippet"]["title"]
        for file in os.listdir(f"data/single_media/"):
            if file.startswith(title) and (file.endswith(".mp4") or file.endswith(".webm")):
                input_path = f"data/single_media/{file}"
                output_path = f"data/single_media/{os.path.splitext(file)[0]}.mp3"
                AudioFileClip(input_path).write_audiofile(output_path, codec='mp3', verbose=False, logger=None)
                os.remove(input_path)
        print(f"Conversion to mp3 completed successfully.")


while True:
    print("(DP) Download Playlist. (D) Download a single video. (PP) Play a playlist. (PS) Play a single video/song. (E) Exit")
    choice=input("> ").lower()
    if choice == "e":
        sys.exit("Exiting program.")
    elif choice == "dp":
        print("Type playlist link")
        i=input("> ")
        filetype = input("Type desired filetype (media or sound): ").lower()
        ydl_opts = {
            'outtmpl': 'data/playlists/%(playlist_title)s/%(title)s.%(ext)s',
            "format": "best[ext=mp4][vcodec!*=av01]/best", 
            'ignoreerrors': True,
            'noplaylist': False,   # ensures full playlist is downloaded
            'quiet': True,
            'no_warnings': True,
            "retries": 10,
        }

        playlist_id = i.split("list=")[-1].split("&")[0]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            ydl.download([i])
        print("Download completed successfully.")
        os.system("cls" if os.name == "nt" else "clear")
        if filetype != "media":
            convert(playlist_id, False, None)
        else:
            print("No conversion needed for mp4 format.")
    elif choice == "d":
        link = input("Type video link > ")
        filetype = input("Type desired filetype (media or sound) > ").lower()
        ydl_opts = {
            'outtmpl': 'data/single_media/%(title)s.%(ext)s',
            "format": "best[ext=mp4][vcodec!*=av01]/best", 
            'ignoreerrors': True,
            'noplaylist': False,   # ensures full playlist is downloaded
            'quiet': True,
            'no_warnings': True,
            "retries": 10,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            ydl.download([link])
        print("Download completed successfully.")
        if filetype != "media":
            video_id = link.split("v=")[-1].split("&")[0]
            convert(None, True, video_id)
        else:
            print("No conversion needed for mp4 format.")
    elif choice == "pp":
        last_press = 0
        cooldown = 0.5  # seconds — tweak this to taste
        print("Type playlist name")
        pname=input("> ")
        ptype = input("Is the playlist made out of (M) media files or (S) sound files? > ").lower()
        mode = input("(N) Normal. (S) Shuffle. > ").lower()
        loop = input("Loop? (y/n) > ").lower()
        files = os.listdir(f"data/playlists/{pname}/")
        
        if mode == "s":
            random.shuffle(files)
        else:
            pass
        if ptype == "m":
            for file in files:
                video_id = file.split(".")[0]
                clip = VideoFileClip(f"data/playlists/{pname}/{file}")
                pygame.init()
                screen = pygame.display.set_mode(clip.size)
                pygame.display.set_caption("Video Player")
                clock = pygame.time.Clock()
                fps = clip.fps
                frames = clip.iter_frames()
                paused = False
                with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    clip.audio.write_audiofile(tmp.name, fps=44100, verbose=False, logger=None) #type: ignore
                    tmp_path = tmp.name
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            clip.close()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                paused = not paused
                    if not paused:
                        pygame.mixer.music.unpause()
                        try:
                            frame = next(frames)
                            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
                            screen.blit(frame_surface, (0, 0))
                            pygame.display.update()
                            clock.tick(fps)
                        except StopIteration:
                            break
                    else:
                        pygame.mixer.music.pause()
                pygame.mixer.music.stop()
                os.remove(tmp_path)
                pygame.quit()
                clip.close()
        else:
            for file in files:
                os.system("cls" if os.name == "nt" else "clear")
                print(f"Now playing: {file}")
                print("=================================================")
                print("Press 's' to stop playback, 'p' to pause, 'n' to go to next track: ")
                pygame.mixer.init()
                pygame.mixer.music.load(f"data/playlists/{pname}/{file}")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if not is_console_focused():
                        continue
                    now = time.time()
                    if keyboard.is_pressed('s') and now - last_press > cooldown:
                        pygame.mixer.music.stop()
                        last_press = now
                        break
                    elif keyboard.is_pressed('p') and now - last_press > cooldown:
                        last_press = now
                        pygame.mixer.music.pause()
                        input("Press Enter to unpause...")
                        pygame.mixer.music.unpause()
                    elif keyboard.is_pressed('n') and now - last_press > cooldown:
                        last_press = now
                        pygame.mixer.music.stop()
                        break
                if keyboard.is_pressed('s'):
                    break
                if loop == "y":
                    files.append(file)
                if mode == "s":
                    random.shuffle(files)
    elif choice == "ps":
        last_press = 0
        cooldown = 0.5  # seconds — tweak this to taste
        print("Is sound in (P) playlists or (S) in the single media folder?")
        loc=input("> ").lower()
        if loc == "p":
            print("Type playlist name")
            pname=input("> ")
            files = os.listdir(f"data/playlists/{pname}/")
            print("Type sound name (with extension)")
            sname=input("> ")
            if sname not in files:
                print("Sound not found in the specified playlist.")
                continue
            print("Is it a video or a sound file? (V/S)")
            ftype = input("> ").lower()
            if ftype == "v":
                video_id = sname.split(".")[0]
                clip = VideoFileClip(f"data/playlists/{pname}/{sname}")
                pygame.init()
                screen = pygame.display.set_mode(clip.size)
                pygame.display.set_caption("Video Player")
                clock = pygame.time.Clock()
                fps = clip.fps
                frames = clip.iter_frames()
                paused = False
                with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    clip.audio.write_audiofile(tmp.name, fps=44100, verbose=False, logger=None) #type: ignore
                    tmp_path = tmp.name
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            clip.close()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                paused = not paused
                    if not paused:
                        pygame.mixer.music.unpause()
                        try:
                            frame = next(frames)
                            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
                            screen.blit(frame_surface, (0, 0))
                            pygame.display.update()
                            clock.tick(fps)
                        except StopIteration:
                            break
                    else:
                        pygame.mixer.music.pause()
                pygame.mixer.music.stop()
                os.remove(tmp_path)
                pygame.quit()
                clip.close()
            elif ftype == "s":
                pygame.mixer.init()
                pygame.mixer.music.load(f"data/playlists/{pname}/{sname}")
                pygame.mixer.music.play()
                print("Press 's' to stop playback, 'p' to pause: ")
                while pygame.mixer.music.get_busy():
                    if not is_console_focused():
                        continue
                    now = time.time()
                    if keyboard.is_pressed('s') and now - last_press > cooldown:
                        pygame.mixer.music.stop()
                        last_press = now
                        break
                    elif keyboard.is_pressed('p') and now - last_press > cooldown:
                        last_press = now
                        pygame.mixer.music.pause()
                        input("Press Enter to unpause...")
                        pygame.mixer.music.unpause()
        elif loc == "s":
            print("Type file name (with extension)")
            sname=input("> ")
            if not os.path.exists(f"data/single_media/{sname}"):
                print("file not found in folder.")
                continue
            print("Is it a video or a file file? (V/S)")
            ftype = input("> ").lower()
            if ftype == "v":
                video_id = sname.split(".")[0]
                clip = VideoFileClip(f"data/single_media/{sname}")
                pygame.init()
                screen = pygame.display.set_mode(clip.size)
                pygame.display.set_caption("Video Player")
                clock = pygame.time.Clock()
                fps = clip.fps
                frames = clip.iter_frames()
                paused = False
                with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    clip.audio.write_audiofile(tmp.name, fps=44100, verbose=False, logger=None) #type: ignore
                    tmp_path = tmp.name
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            clip.close()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                paused = not paused
                    if not paused:
                        pygame.mixer.music.unpause()
                        try:
                            frame = next(frames)
                            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
                            screen.blit(frame_surface, (0, 0))
                            pygame.display.update()
                            clock.tick(fps)
                        except StopIteration:
                            break
                    else:
                        pygame.mixer.music.pause()
                pygame.mixer.music.stop()
                os.remove(tmp_path)
                pygame.quit()
                clip.close()
            elif ftype == "s":
                print(f"Now playing: {sname}")
                pygame.mixer.init()
                pygame.mixer.music.load(f"data/single_media/{sname}")
                pygame.mixer.music.play()
                print("Press 's' to stop playback, 'p' to pause: ")
                while pygame.mixer.music.get_busy():
                    if not is_console_focused():
                        continue
                    now = time.time()
                    if keyboard.is_pressed('s') and now - last_press > cooldown:
                        pygame.mixer.music.stop()
                        last_press = now
                        break
                    elif keyboard.is_pressed('p') and now - last_press > cooldown:
                        last_press = now
                        pygame.mixer.music.pause()
                        input("Press Enter to unpause...")
                        pygame.mixer.music.unpause()