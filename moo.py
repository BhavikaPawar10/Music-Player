import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import fnmatch
import time
import pygame

pygame.init()
clock = pygame.time.Clock()
playing = False
current_song_index = -1

# Update the list with the selected song name from the list
def update_song_name(event):
    global current_song_index
    selected_song = listbox.get(listbox.curselection())
    song_name.config(text=selected_song)
    current_song_index = listbox.curselection()[0]  # Update the current song index
    global playing
    playing = False  # Stop the previous song if playing
    play_song(selected_song)

# Play or pause the song based on selection
def play_pause():
    global playing
    if not playing:
        pygame.mixer.music.unpause()
        playing = True
        play_button.config(text="⏸️")
    else:
        pygame.mixer.music.pause()
        playing = False
        play_button.config(text="▶️")

# Play the next song on forward button click
def play_next():
    global current_song_index
    next_song_index = (current_song_index + 1) % listbox.size()
    listbox.selection_clear(0, tk.END)  # Clear previous selection
    listbox.selection_set(next_song_index)  # Select the next song
    listbox.event_generate("<<ListboxSelect>>")  # Trigger the selection event

# Play the previous song on the backward button click
def play_previous():
    global current_song_index
    previous_song_index = (current_song_index - 1) % listbox.size()
    listbox.selection_clear(0, tk.END)  # Clear previous selection
    listbox.selection_set(previous_song_index)  # Select the previous song
    listbox.event_generate("<<ListboxSelect>>")  # Trigger the selection event

# Play the selected song
def play_song(song_path):
    global playing
    pygame.mixer.init()
    pygame.mixer.music.load("musics" + "\\" + song_path)
    pygame.mixer.music.play()
    playing = True
    play_button.config(text="⏸️")
    start_time_label.config(text="Start: 00:00")  # Reset start time when a new song is played
    song_length = pygame.mixer.Sound("musics" + "\\" + song_path).get_length()
    end_time_label.config(text=f"End: {time_format(song_length)}")

# Update the progress bar's progress while playing
def update_progress_bar():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy() and playing:
        current_position = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
        progress_bar.step(current_position - progress_bar['value'])
        progress_bar['value'] = current_position
    canvas.after(1000, update_progress_bar)  # Update every 1 second (1000 milliseconds)

#changing the time format 
def time_format(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{int(s):02d}"

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("1200x700")
canvas.config(bg='black')

frame1 = tk.Frame(canvas, bg="lightblue")
frame2 = tk.Frame(canvas, bg="lightgreen")

frame1.pack(side="left", fill="both", expand=True)
frame2.pack(side="right", fill="both", expand=True)

# music image
image = Image.open("image.png")
image = image.resize((400, 400))
photo = ImageTk.PhotoImage(image)

label1 = tk.Label(frame1, image=photo)
label1.image = photo
label1.grid(row=0, column=2, pady=30, padx=80, rowspan=3, columnspan=3)

#progress bar
progress_bar = ttk.Progressbar(frame1, mode="indeterminate", length=600)
progress_bar.grid(row=3, column=2, columnspan=3, pady=10, padx=30)

start_time_label = tk.Label(frame1, text="Start:", font=("Arial", 12), fg="black", bg="lightblue")
start_time_label.grid(row=4, column=2, sticky="nw")

end_time_label = tk.Label(frame1, text="End:", font=("Arial", 12), fg="black", bg="lightblue")
end_time_label.grid(row=4, column=4, sticky="ne")

canvas.after(1000, update_progress_bar)

#playing song name
song_name = tk.Label(frame1, text="", font=("Arial", 15), fg="black", bg="lightblue")
song_name.grid(row=5, column=2, columnspan=3, sticky="nsew", pady=20)

# buttons with symbols
backward_button = tk.Button(frame1, text="⏮️", font=("Arial", 24), bg="lightblue",bd=0,command=play_previous)
backward_button.grid(row=6, column=2)

play_button = tk.Button(frame1, text="▶️", font=("Arial", 24), bg="lightblue",bd=0,command=play_pause)
play_button.grid(row=6, column=3)

forward_button = tk.Button(frame1, text="⏭️", font=("Arial", 24), bg="lightblue",bd=0,command=play_next)
forward_button.grid(row=6, column=4)

# music list
listbox = tk.Listbox(frame2, selectmode=tk.SINGLE, width=40, height=40, font=("Arial", 15))
listbox.pack(pady=20)

rootpath = "musics"
pattern = "*.mp3"

for root, dirs, files in os.walk(rootpath):
    for filename in(files):
        listbox.insert(tk.END, filename)

listbox.bind('<<ListboxSelect>>', update_song_name)
update_progress_bar() 

canvas.mainloop()
