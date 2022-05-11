from tkinter import *
from tkinter import messagebox, ttk
import multiprocessing
import os

import pytube.exceptions
from pytube import YouTube, Playlist

from youtube import YouTube_downloader, YouTube_process
from playlist import Playlist_process, Playlist_downloader, PrivatePlaylistError
from others import distinguisher


def show_info(url):
    try:
        if distinguisher(url) == "video":
            yt = YouTube(url)

            secs = yt.length % 60
            minutes = (yt.length - secs) / 60

            messagebox.showinfo("Video",
                                f"Title: {yt.title}\nBy: {yt.author}\nViews: {yt.views}\nLength {minutes}:{secs}")
        else:

            if distinguisher(url) == "private":
                raise PrivatePlaylistError

            p = Playlist(url)

            messagebox.showinfo("Playlist",
                                f"Title: {p.title}\nOwner: {p.owner}\nViews: {p.views}\nLength: {p.length}")

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')

    except PrivatePlaylistError:
        messagebox.showerror('Error', 'Playlist is private')

    except KeyError:
        messagebox.showerror('Error', 'Enter valid url')


def download(url, audio_only=False, file_extension="mp4", filename=None):
    if distinguisher(url) == "playlist":

        Playlist_process(url, audio_only, file_extension)

    else:

        YouTube_process(url, audio_only, file_extension, filename)


def main():
    window = Tk()
    window.geometry('500x500')

    audio = BooleanVar()
    audio.set(False)

    Label(window, bg='black').place(
        x=0, y=220, width=500, height=5)

    Label(window, text="Options:", font=25).place(
        x=210, y=240)

    audio_box = Checkbutton(window, text="Only audio", font=1, var=audio)

    audio_box.place(x=0, y=280)

    Label(window, text="File extension:", font=1).place(x=0, y=325)

    combo = ttk.Combobox(window)
    combo['values'] = ("mp4", "webm", "3gpp")
    combo.current(0)
    combo.place(x=0, y=360)

    Label(window, text="Enter URL of YouTube video", font=1).place(width=500, height=30, x=0, y=70)

    URL = Entry(window)

    URL.place(width=250, height=30, x=125, y=100)

    filename = Entry(window)

    filename.place(x=0, y=425, width=140, height=20)

    Button(window, text='Download!',
           command=lambda: download(URL.get(), audio.get(), combo.get(), filename.get())).place(
        width=100,
        height=30, x=150,
        y=140)

    Button(window, text="Show info", command=lambda: show_info(URL.get())).place(width=100, height=30, x=250, y=140)

    Label(window, text="Enter filename:", font=1).place(x=0, y=395)

    window.mainloop()


def tkinter_process():
    p = multiprocessing.Process(target=main)

    p.start()


if __name__ == '__main__':
    tkinter_process()
