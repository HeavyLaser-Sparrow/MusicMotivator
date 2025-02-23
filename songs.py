import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pygame
import threading
import time
import json
import os
import random

SAVE_FILE = "progress.json"

def calculate_minutes(lessons, exercises, labs):
    return lessons * 5 + exercises * 10 + labs * 20


class MusicMotivator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lesson Music Motivator")
        self.minutes_bank = 0
        self.total_lessons = 0
        self.total_exercises = 0
        self.total_labs = 0
        self.current_song_playing = False
        self.is_paused = False
        self.song_list = []
        self.current_song_index = -1
        self.last_played_index = None
        self.last_update_time = time.time()

        pygame.mixer.init()
        self.load_progress()
        self.create_widgets()
        self.update_timer()
        self.check_song_end()

    def create_widgets(self):
        tk.Label(self.root, text="Additional Lessons Completed (5 min each):").grid(row=0, column=0)
        self.lesson_entry = tk.Entry(self.root)
        self.lesson_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Additional Guided Exercises Completed (10 min each):").grid(row=1, column=0)
        self.exercise_entry = tk.Entry(self.root)
        self.exercise_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Additional Unit Labs Completed (20 min each):").grid(row=2, column=0)
        self.lab_entry = tk.Entry(self.root)
        self.lab_entry.grid(row=2, column=1)

        self.add_minutes_button = tk.Button(self.root, text="Add Minutes", command=self.add_minutes)
        self.add_minutes_button.grid(row=3, column=0, columnspan=2)

        self.minutes_label = tk.Label(self.root, text=f"Minutes Left: {int(self.minutes_bank)}")
        self.minutes_label.grid(row=4, column=0, columnspan=2)

        self.song_label = tk.Label(self.root, text="Current Song: None")
        self.song_label.grid(row=5, column=0, columnspan=2)

        self.play_button = tk.Button(self.root, text="Play Song", command=self.load_and_play_song)
        self.play_button.grid(row=6, column=0)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_song)
        self.pause_button.grid(row=6, column=1)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_song)
        self.resume_button.grid(row=6, column=2)

        self.stop_button = tk.Button(self.root, text="Stop Song", command=self.stop_song)
        self.stop_button.grid(row=6, column=3)

        tk.Label(self.root, text="Playback Options:").grid(row=7, column=0)
        self.playback_mode = ttk.Combobox(self.root, values=["Normal", "Shuffle", "Repeat"], state="readonly")
        self.playback_mode.set("Normal")
        self.playback_mode.grid(row=7, column=1, columnspan=3)
        self.playback_mode.bind("<<ComboboxSelected>>", self.update_playback_mode)

        self.load_playlist_button = tk.Button(self.root, text="Load Playlist from Folder", command=self.load_playlist_from_folder)
        self.load_playlist_button.grid(row=8, column=0, columnspan=4)

    def add_minutes(self):
        try:
            lessons = int(self.lesson_entry.get() or 0)
            exercises = int(self.exercise_entry.get() or 0)
            labs = int(self.lab_entry.get() or 0)

            self.total_lessons += lessons
            self.total_exercises += exercises
            self.total_labs += labs

            self.minutes_bank += calculate_minutes(lessons, exercises, labs)
            self.update_minutes_label()
            self.save_progress()
        except ValueError:
            self.minutes_label.config(text="Please enter valid numbers.")

    def update_minutes_label(self):
        self.minutes_label.config(text=f"Minutes Left: {int(self.minutes_bank)}")

    def load_playlist_from_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.song_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]
            if not self.song_list:
                messagebox.showinfo("No Songs Found", "No .mp3 files were found in the selected folder.")
            else:
                self.current_song_index = -1
                messagebox.showinfo("Playlist Loaded", f"Loaded {len(self.song_list)} .mp3 files from the folder.")

    def load_and_play_song(self):
        if self.minutes_bank <= 0:
            self.minutes_label.config(text="Not enough minutes to play music.")
            return

        if not self.song_list:
            self.load_playlist_from_folder()

        if self.song_list:
            if self.playback_mode.get() == "Shuffle":
                self.select_next_shuffled_song()
            else:
                self.current_song_index = 0
            self.play_song_by_index(self.current_song_index)

    def select_next_shuffled_song(self):
        if len(self.song_list) > 1:
            possible_indices = [i for i in range(len(self.song_list)) if i != self.last_played_index]
            self.current_song_index = random.choice(possible_indices)
        else:
            self.current_song_index = 0
        self.last_played_index = self.current_song_index

    def play_song_by_index(self, index):
        if self.minutes_bank <= 0:
            self.minutes_label.config(text="Not enough minutes to play music.")
            return

        if 0 <= index < len(self.song_list):
            file_path = self.song_list[index]
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.song_label.config(text=f"Current Song: {file_path.split('/')[-1]}")
                self.current_song_playing = True
                self.is_paused = False
            except pygame.error:
                self.song_label.config(text="Error loading file. Unsupported format.")

    def update_playback_mode(self, event):
        if self.current_song_playing:
            current_position = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.stop()
            self.play_song_by_index(self.current_song_index)
            pygame.mixer.music.set_pos(current_position)

    def pause_song(self):
        if self.current_song_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume_song(self):
        if self.current_song_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def check_song_end(self):
        if not pygame.mixer.music.get_busy() and self.current_song_playing and not self.is_paused:
            self.handle_song_end()
        self.root.after(1000, self.check_song_end)

    def handle_song_end(self):
        mode = self.playback_mode.get()
        if mode == "Repeat":
            self.play_song_by_index(self.current_song_index)
        elif mode == "Shuffle":
            self.select_next_shuffled_song()
            self.play_song_by_index(self.current_song_index)
        else:
            self.current_song_index += 1
            if self.current_song_index < len(self.song_list):
                self.play_song_by_index(self.current_song_index)
            else:
                self.stop_song()

    def update_timer(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.last_update_time = current_time

        if pygame.mixer.music.get_busy() and self.minutes_bank > 0 and not self.is_paused:
            self.minutes_bank = max(0, self.minutes_bank - elapsed_time / 60)
            self.update_minutes_label()
            self.save_progress()

            if self.minutes_bank <= 0:
                self.stop_song()
        self.root.after(1000, self.update_timer)

    def stop_song(self):
        pygame.mixer.music.stop()
        self.current_song_playing = False
        self.song_label.config(text="Current Song: None")
        self.update_minutes_label()
        self.save_progress()

    def save_progress(self):
        progress = {
            "total_lessons": self.total_lessons,
            "total_exercises": self.total_exercises,
            "total_labs": self.total_labs,
            "minutes_bank": self.minutes_bank
        }
        with open(SAVE_FILE, "w") as file:
            json.dump(progress, file)

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file:
                progress = json.load(file)
                self.total_lessons = progress.get("total_lessons", 0)
                self.total_exercises = progress.get("total_exercises", 0)
                self.total_labs = progress.get("total_labs", 0)
                self.minutes_bank = progress.get("minutes_bank", 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicMotivator(root)
    root.mainloop()
