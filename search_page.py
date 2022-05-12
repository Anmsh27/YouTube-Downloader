from pytube import Search, YouTube
from tkinter import *
from youtube import YouTube_process
import multiprocessing
from show_info import show_info


class SearchResult():
    def __init__(self, obj):
        self.obj = obj

    def show(self, frame):
        return_obj = Frame(frame, width=500, height=50, highlightthickness=1, highlightbackground='black')
        return_obj.pack()
        Label(return_obj, text=self.obj.title).place(x=0, y=0)
        butt1 = Button(return_obj, text="Download", command=lambda: YouTube_process(None, yt_obj=self.obj))
        butt1.place(x=400, y=0, height=25)
        butt2 = Button(return_obj, text="Show info", command=lambda: show_info(None, yt_obj=self.obj))
        butt2.place(x=400, y=25, height=24)


def search(searchword, frame):
    s = Search(searchword)

    res_list = []

    for vid in s.results:
        res_list.append(SearchResult(vid))

    for res in res_list:
        res.show(frame)


def search_page(window):
    URL = Entry(window)

    URL.place(width=300, height=30, x=100, y=100)

    frame = Frame(window)
    frame.place(x=0, y=200, width=500, height=350)

    Label(window, text="Enter search", font=30).place(width=200, height=30, x=150, y=70)

    Label(window, bg='black').place(width=500, height=5, x=0, y=180)

    Button(window, text="Search", command=lambda: search(URL.get(), frame)).place(width=100, height=30, x=200, y=130)
