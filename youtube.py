import os

from pytube import YouTube
from tkinter import *
from tkinter import ttk,messagebox
import multiprocessing
import pytube.exceptions

class AudioVideoException(Exception):
    pass

def YouTube_process(url, audio_only=False, file_extension="mp4", filename=None, video_only=False, yt_obj=None):
    p = multiprocessing.Process(target=YouTube_downloader, args=(url, audio_only, file_extension, filename, video_only, yt_obj,))

    p.start()


def YouTube_downloader(url, audio_only=False, file_extension="mp4", filename=None, video_only=False, yt_obj=None):

    if yt_obj:
        yt_obj.streams.get_highest_resolution().download(output_path=os.getcwd())
        print("Done")
        return

    try:

        if video_only and audio_only:
            raise AudioVideoException

        yt = YouTube(url)

        vid_title = ""
        for word in yt.title.split(" "):
            vid_title = vid_title + word

        filename_final = ""
        if filename:
            for word in filename.split(" "):
                filename_final = filename_final + word

        if audio_only:
            yt.streams.get_audio_only().download(filename=f'{filename_final}.mp3' if filename else 'youtube_video.mp3')

            print("Done")

            messagebox.showinfo('Video Downloader', 'Done!')


        else:

            try:

                if video_only:
                    yt.streams.filter(file_extension=file_extension,
                                      only_audio=False).get_highest_resolution().download(
                        filename=f'{filename_final}.{file_extension}' if filename else f'{vid_title}.{file_extension}')

                else:
                    yt.streams.filter(file_extension=file_extension, only_audio=False).get_highest_resolution().download(
                        filename=f'{filename_final}.{file_extension}' if filename else f'{vid_title}.{file_extension}')

            except AttributeError:
                messagebox.showerror('Error', 'Enter valid file extension')

            print("Done")

            messagebox.showinfo('Video Downloader', 'Done!')

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')

    except pytube.exceptions.PytubeError as e:
        messagebox.showerror('Error', str(e))

    except AudioVideoException:
        messagebox.showerror('Error', 'Cannot have only audio and only video\nplease select only one or none')

