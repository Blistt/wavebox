import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

class RadioApp:
    def __init__(self, master):
        self.master = master
        master.title("WaveBox")

        # Menu screen
        self.label = tk.Label(master, text="Please select an audio file and radio type:")
        self.label.pack()

        self.insert_button = tk.Button(master, text="Insert Audio File", command=self.insert_file)
        self.insert_button.pack()

        self.radio_selection = tk.StringVar()
        self.radio_selection.set("FM")

        self.am_radio = tk.Radiobutton(master, text="FM", variable=self.radio_selection, value="FM")
        self.am_radio.pack()

        self.fm_radio = tk.Radiobutton(master, text="AM", variable=self.radio_selection, value="AM")
        self.fm_radio.pack()

        self.next_button = tk.Button(master, text="Scan", command=self.show_result, state=tk.DISABLED)
        self.next_button.pack()

        self.file_loaded_label = tk.Label(master, text="")
        self.file_loaded_label.pack()

    def insert_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
        if filename:
            self.audio_filename = filename
            self.next_button.config(state=tk.NORMAL)
            self.file_loaded_label.config(text=f"File loaded: {os.path.basename(filename)}")

    def show_result(self):
        # Generate some example radio stations
        radio_stations = self.generate_radio_stations()

        # Match closest radio station
        closest_station = self.match_audio_to_station(radio_stations)

        # Display result
        result_window = tk.Toplevel(self.master)
        result_window.title("WaveBox")
        result_window.geometry("300x100")

        closest_label = tk.Label(result_window, text="Closest Radio Station:")
        closest_label.pack()

        closest_station_label = tk.Label(result_window, text=closest_station)
        closest_station_label.pack()

        # Button for listening to the closest radio station
        listen_button = tk.Button(result_window, text="Listen", command=lambda: self.listen_to_station(closest_station))
        listen_button.pack()

    def generate_radio_stations(self):
        # Generate some example radio stations
        radio_stations = ["88.5",
                      "89.5",
                      "92.3",
                      "93.1",
                      "93.5",
                      "93.9",
                      "94.7",
                      "95.5",
                      "96.3",
                      "97.5",
                      "98.3",
                      "99.5",
                      "99.9",
                      "100.7",
                      "102.1",
                      "103.5",
                      "104.3",
                      "105.1",
                      "105.9",
                      "106.7"]
        return radio_stations
    
    def listen_to_station(self, station):
        # Create a new window for displaying live feed
        live_feed_window = tk.Toplevel(self.master)
        live_feed_window.title(f"Live Feed: {station}")
        live_feed_window.geometry("300x100")

        # Here you can embed a media player or use a streaming service to play the radio station
        # For demonstration purpose, let's just display a message
        message_label = tk.Label(live_feed_window, text=f"Now playing: {station}")
        message_label.pack()

        # Button to stop listening and return to the main menu
        stop_button = tk.Button(live_feed_window, text="Stop Listening", command=live_feed_window.destroy)
        stop_button.pack()

    def match_audio_to_station(self, radio_stations):
        #WaveBox function should go here.
        return radio_stations[0]

def main():
    root = tk.Tk()
    root.geometry("350x130")
    app = RadioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
