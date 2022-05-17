from tkinter import *
from tkinter import messagebox, ttk
import multiprocessing
import os

import pytube.exceptions
from pytube import YouTube, Playlist
from show_info import show_info

from youtube import YouTube_process
from playlist import Playlist_process, PrivatePlaylistError
from distinguisher import distinguisher

from search_page import search_page


def download(url, audio_only=False, file_extension="mp4", filename=None, video_only=False):
    if distinguisher(url) == "playlist":

        Playlist_process(url, audio_only, file_extension)

    else:

        YouTube_process(url, audio_only, file_extension, filename, video_only)


def main_page(window):
    audio = BooleanVar()
    audio.set(False)

    video = BooleanVar()
    video.set(False)

    Label(window, bg='black').place(
        x=0, y=220, width=500, height=5)

    Label(window, text="Options:", font=25).place(
        x=210, y=240)

    audio_box = Checkbutton(window, text="Only audio", font=1, var=audio)

    audio_box.place(x=0, y=280)

    video_box = Checkbutton(window, text="Only Video", font=1, var=video)

    video_box.place(x=175, y=280)

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
           command=lambda: download(URL.get(), audio.get(), combo.get(), filename.get(), video.get())).place(
        width=100,
        height=30, x=150,
        y=140)

    Button(window, text="Show info", command=lambda: show_info(URL.get())).place(width=100, height=30, x=250, y=140)

    Label(window, text="Enter filename:", font=1).place(x=0, y=395)


def main():
    window = Tk()
    window.geometry('500x500')
    window.resizable(False, False)
    window.title('Youtube Downloader')
    window.iconbitmap('youtube.ico')

    search_frame = Frame(window)
    main_frame = Frame(window)

    def switch1():
        main_frame.place(x=0, y=0, width=500, height=500)
        search_frame.place_forget()
        main_page(main_frame)

    def switch2():
        search_frame.place(x=0, y=0, width=500, height=500)
        main_frame.place_forget()
        search_page(search_frame)

    Button(window, text="Search", command=lambda: switch2()).place(x=0, y=0, width=100, height=30)

    Button(window, text="Main", command=lambda: switch1()).place(x=400, y=0, width=100, height=30)

    window.mainloop()


def tkinter_process():
    p = multiprocessing.Process(target=main)

    p.start()


if __name__ == '__main__':
    tkinter_process()
