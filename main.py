from pytube import Search, YouTube
from urllib.request import urlopen
import music_tag
import os


path = os.getcwd() + "\\musiques"


def run1():
    active = True
    while active:
        search = str(input("Enter title/link of a song >>> "))

        if search[0:5] == "https":
            video_ytb = YouTube(search)
        else:
            videos_ytb = Search(search).results
            print("We found : ")
            for i in range(len(videos_ytb)):
                print(str(i + 1) + ") " + videos_ytb[i].title + " de : " + videos_ytb[i].author)

            n = int(input("Which one do you want to save? >>> "))
            video_ytb = videos_ytb[n - 1]
        download_mp3(video_ytb)
        active = str(input("Do you want to download an other music? >>> ")) == "y"
        print("__________________________________________________________")


def edit_mp3_data(video_ytb, file_name):
    thumbnail_url = video_ytb.thumbnail_url
    artist = video_ytb.author
    f = music_tag.load_file(path + "\\" + file_name)
    f["artist"] = artist
    img = urlopen(thumbnail_url).read()
    f["artwork"] = img
    f.save()


def download_mp3(video_ytb):
    video = video_ytb.streams.filter(only_audio=True).first()

    # Télécharge le fichier et retourne le path sous forme de chaîne de caractères.
    out_file_name = video.download(output_path=path)

    # .mp4 to .mp3
    base = os.path.splitext(out_file_name)[0]
    new_file_name = base + ".mp3"
    os.rename(out_file_name, new_file_name)

    edit_mp3_data(video_ytb, os.path.basename(new_file_name))

    # Success
    print(video_ytb.title + " has been downloaded! :D")


run1()
