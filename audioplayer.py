#imports
import os
import vlc
import tkinter as tk
from tkinter import *
from tkinter import filedialog, simpledialog, Toplevel, Button, SINGLE
from PIL import Image, ImageTk

# tkinter initialization
t = Tk()
t.geometry("700x700")
t.title("Audio Player")

file_list = []
playlists = []

class AddToPlaylistWindow:
    def __init__(self):
        self.popup = None
        self.song_list = None

    def open(self):
        self.popup = Toplevel()
        self.popup.title("Select Song: ")
        self.popup.geometry("400x200")
        self.song_list = Listbox(self.popup, selectmode=SINGLE)
        self.song_list.pack(fill="both", expand=True)

        for item in file_list:
            self.song_list.insert(END, item)

        select_button = Button(self.popup, text="Select", command=self.selectPlaylist)
        select_button.pack()

    def selectPlaylist(self):
        selected_item = self.song_list.get(self.song_list.curselection())
        self.popup.destroy()

        select_playlist_window = SelectPlaylistWindow(selected_item)
        select_playlist_window.open()

class SelectPlaylistWindow:
    def __init__(self, selected_item):
        self.popup = None
        self.playlist_list = None
        self.selected_item = selected_item

    def open(self):
        self.popup = Toplevel()
        self.popup.title("Select Playlist: ")
        self.popup.geometry("400x200")
        self.playlist_list = Listbox(self.popup, selectmode=SINGLE)
        self.playlist_list.pack(fill="both", expand=True)

        for item in playlists:
            self.playlist_list.insert(END, item[0])

        select_button = Button(self.popup, text="Select", command=self.choosePlaylist)
        select_button.pack()

    def choosePlaylist(self):
        selected_playlist = self.playlist_list.get(self.playlist_list.curselection())
        selected_playlist_index = next((i for i, playlist in enumerate(playlists) if playlist[0] == selected_playlist), None)

        if selected_playlist_index is not None:
            playlists[selected_playlist_index][1].append(self.selected_item)
            print(playlists[selected_playlist_index][1])

        self.popup.destroy()

def fileInput():
    file_path = filedialog.askopenfilename()
    file_list.append(file_path)
    file_list_widget.insert(END, file_path)

def playAudio(event):
    index = file_list_widget.curselection()
    if index:
        p = vlc.MediaPlayer(file_list[index[0]])
        p.play()
        print("Now playing: ")

def createPlaylist():
    playlist_name = simpledialog.askstring("Playlist Title", "Playlist Title: ")
    playlist = [playlist_name, []]
    playlists.append(playlist)
    print(playlists)

def addToPlaylist():
    add_to_playlist_window = AddToPlaylistWindow()
    add_to_playlist_window.open()

add_file = tk.Button(t, text="Add File", command=fileInput)
add_file.pack()
create_playlist = tk.Button(text="Create Playlist", command=createPlaylist)
create_playlist.pack()
add_to_playlist = tk.Button(text="Add to Playlist", command=addToPlaylist)
add_to_playlist.pack()
file_list_widget = Listbox(t)
file_list_widget.pack(fill="x")
file_list_widget.bind("<Button-1>", playAudio)

t.mainloop()
