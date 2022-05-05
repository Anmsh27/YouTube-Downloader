from tkinter import *
from tkinter import messagebox, ttk
import multiprocessing
import os

import pytube.exceptions
from pytube import YouTube, Playlist


def YouTube_process(url, audio_only=False, file_extension="mp4"):
    p = multiprocessing.Process(target=YouTube_downloader, args=(url, audio_only, file_extension,))

    p.start()


def YouTube_downloader(url, audio_only=False, file_extension="mp4"):
    try:

        yt = YouTube(url)

        if audio_only:
            yt.streams.get_audio_only().download(filename='youtube_video.mp3')

            messagebox.showinfo('Video Downloader', 'Done!')

        else:
            try:

                yt.streams.filter(file_extension=file_extension, only_video=True).first().download()

            except AttributeError:
                messagebox.showerror('Error', 'Enter valid file extension')

            messagebox.showinfo('Video Downloader', 'Done!')

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')

    except pytube.exceptions.PytubeError as e:
        messagebox.showerror('Error', str(e))


def Playlist_downloader(url, audio_only=False, file_extension="mp4"):
    try:

        p = Playlist(url)

        try:
            os.mkdir(f"{p.title}")
        except FileExistsError:
            pass

        for video in p.videos:

            if audio_only:
                video.streams.get_audio_only().download(output_path=f'{p.title}/')

            else:
                try:

                    video.streams.filter(file_extension=file_extension, only_video=True).first().download(
                        output_path=f'{p.title}/')

                except AttributeError:
                    messagebox.showerror('Error', 'Enter valid file extension')

        messagebox.showinfo('Video Downloader', 'Done!')

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')

    except pytube.exceptions.PytubeError as e:
        messagebox.showerror('Error', str(e))


def Playlist_process(url, audio_only=False, file_extension="mp4"):
    p = multiprocessing.Process(target=Playlist_downloader, args=(url, audio_only, file_extension,))

    p.start()


def distinguisher(url):
    if "&list=" or "playlist" in url:
        return "playlist"
    else:
        return "video"


def show_info(url):
    try:
        if distinguisher(url) == "video":
            yt = YouTube(url)

            secs = yt.length % 60
            minutes = (yt.length - secs) / 60

            messagebox.showinfo("Video",
                                f"Title: {yt.title}\nBy: {yt.author}\nViews: {yt.views}\nLength {minutes}:{secs}")
        else:
            p = Playlist(url)

            messagebox.showinfo("Playlist",
                                f"Title: {p.title}\nOwner: {p.owner}\nViews: {p.views}\nLength: {p.length}")

    except pytube.exceptions.RegexMatchError:
        messagebox.showerror('Error', 'Enter valid url')


def download(url, audio_only=False, file_extension="mp4"):

    if distinguisher(url) == "playlist":

        Playlist_process(url, audio_only, file_extension)

    else:

        YouTube_process(url, audio_only, file_extension)


def main():
    window = Tk()
    window.geometry('500x500')

    audio = BooleanVar()
    audio.set(False)

    Label(window, text="Options:", font=25).place(x=210, y=100)

    audio_box = Checkbutton(window, text="Only audio", font=1, var=audio)

    audio_box.place(x=0, y=125)

    Label(window, text="File extension:", font=1).place(x=0, y=185)

    combo = ttk.Combobox(window)
    combo['values'] = ("mp4", "webm", "3gpp")
    combo.current(0)
    combo.place(x=0, y=220)

    Label(window, text="Enter URL of YouTube video", font=15).place(width=500, height=30, x=0, y=0)

    URL = Entry(window)

    URL.place(width=500, height=30, x=0, y=30)

    Button(window, text='Download!',
           command=lambda: download(URL.get(), audio.get(), combo.get())).place(
        width=100,
        height=30, x=150,
        y=60)

    Button(window, text="Show info", command=lambda: show_info(URL.get())).place(width=100, height=30, x=250, y=60)

    window.mainloop()


def tkinter_process():
    p = multiprocessing.Process(target=main)

    p.start()


if __name__ == '__main__':
    tkinter_process()
