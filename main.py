from tkinter import *
from tkinter import messagebox, ttk
import multiprocessing
import os

import pytube.exceptions
from pytube import YouTube, Playlist


class PrivatePlaylistError(Exception):
    pass


def YouTube_process(url, audio_only=False, file_extension="mp4", filename=None):
    p = multiprocessing.Process(target=YouTube_downloader, args=(url, audio_only, file_extension, filename,))

    p.start()


def YouTube_downloader(url, audio_only=False, file_extension="mp4", filename=None):
    try:

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


def Playlist_downloader(url, audio_only=False, file_extension="mp4"):
    try:

        if distinguisher(url) == "private":
            raise PrivatePlaylistError

        p = Playlist(url)

        try:
            os.mkdir(f"{p.title}")

        except FileExistsError:
            pass

        for video in p.videos:

            vid_title = ""
            for word in p.title.split(" "):
                vid_title = vid_title + word

            if audio_only:
                video.streams.get_audio_only().download(output_path=f'{p.title}/',
                                                        filename=vid_title + "." + file_extension)

            else:
                try:

                    video.streams.filter(file_extension=file_extension,
                                         only_audio=False).get_highest_resolution().download(
                        output_path=f'{p.title}/', filename=vid_title + "." + file_extension)

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


def Playlist_process(url, audio_only=False, file_extension="mp4"):
    p = multiprocessing.Process(target=Playlist_downloader, args=(url, audio_only, file_extension,))

    p.start()


def distinguisher(url):
    if "&list=" in url:
        return "playlist"
    elif "playlist" in url:
        return "private"
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
