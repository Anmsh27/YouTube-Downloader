from playlist import *
from distinguisher import *
from youtube import *

def show_info(url, yt_obj=None):

    if yt_obj:

        secs = yt_obj.length % 60
        minutes = (yt_obj.length - secs) / 60

        messagebox.showinfo("Video",
                            f"Title: {yt_obj.title}\nBy: {yt_obj.author}\nViews: {yt_obj.views}\nLength {minutes}:{secs}")
        return

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

