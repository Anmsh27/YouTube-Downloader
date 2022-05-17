from pytube import Playlist
from  tkinter import messagebox
import multiprocessing
import pytube.exceptions
from distinguisher import distinguisher
import os

class PrivatePlaylistError(Exception):
    pass


def Playlist_downloader(url, audio_only=False, file_extension="mp4", filepath=None):
    try:

        if distinguisher(url) == "private":
            raise PrivatePlaylistError

        p = Playlist(url)

        for video in p.videos:

            vid_title = ""
            for word in p.title.split(" "):
                vid_title = vid_title + word

            if audio_only:
                video.streams.get_audio_only().download(output_path=filepath if filepath else None,
                                                        filename=vid_title + "." + file_extension)

            else:
                try:

                    video.streams.filter(file_extension=file_extension,
                                         only_audio=False).get_highest_resolution().download(
                        output_path=filepath if filepath else None, filename=vid_title + "." + file_extension)

                except AttributeError:
                    messagebox.showerror('Error', 'Enter valid file extension')

        print("Done")

        messagebox.showinfo('Video Downloader', 'Done!')

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')

    except pytube.exceptions.PytubeError as e:
        messagebox.showerror('Error', str(e))

    except PrivatePlaylistError:
        messagebox.showerror('Error', 'Playlist is private')

    except KeyError:
        messagebox.showerror('Error', 'Enter valid url')


def Playlist_process(url, audio_only=False, file_extension="mp4", filepath=None):
    p = multiprocessing.Process(target=Playlist_downloader, args=(url, audio_only, file_extension, filepath,))

    p.start()

