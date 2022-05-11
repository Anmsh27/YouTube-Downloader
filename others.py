
def distinguisher(url):
    if "&list=" in url:
        return "playlist"
    elif "playlist" in url:
        return "private"
    else:
        return "video"