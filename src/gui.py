import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

from datetime import timedelta
from PIL import Image, ImageTk
from random import choice
from threading import Thread
import traceback

from wraplabel import WrapLabel
from song import Song, NoSongFound
from loadfont import loadfont
from lyrics import get_timestamp_lyric, fetch_parsed_lyrics
from spotify_client import create_spotify_client

FONT = "Circular Std Book"
FONT_BOLD = "Circular Std Bold"
FONT_LIGHT = "Circular Std Light"

class MainUi(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Load custom fonts into memory
        loadfont("assets/font.otf", private=True)
        loadfont("assets/font_bold.otf", private=True)
        loadfont("assets/font_light.otf", private=True)

        self.top_menu = TopMenu(master=self, bootstyle=DEFAULT)
        self.top_menu.pack(side=TOP, fill=BOTH, expand=YES)
        
        self.bottom_menu = BottomMenu(master=self, bootstyle=SECONDARY)
        self.bottom_menu.pack(side=TOP, fill=X)

        self.spotify = create_spotify_client()
        raw_data = self.spotify.currently_playing()

        if raw_data == None:
            self.current_song = NoSongFound()
        else:
            self.current_song = Song(raw_data=raw_data)

        self.previous_lyric_index = None

        self.lyrics_loaded = False

        self.bottom_menu.song_label.update_song(self.current_song)
        
        self.after(1, self.song_changed)

        #Start the update_current_song loop in a separate thread
        Thread(target=self.update_current_song, daemon=True).start()

        self.after(10, self.loop)


    def song_changed(self):
        self.lyrics_loaded = False

        self.previous_lyric_index = None

        self.bottom_menu.song_label.update_song(self.current_song)

        self.top_menu.display_message("Fetching the lyrics for this song...")

        if self.current_song.type == "track":
            self.lyrics = fetch_parsed_lyrics(song_name=self.current_song.name,
                                              artist=self.current_song.artists[0],
                                              allow_plain_format=False)

            if self.lyrics == None:
                with open("assets/notfoundmsgs.txt", "r") as f:
                    not_found_message = choice(f.readlines()).strip()+"\n"*2
                
                self.top_menu.display_message(message=not_found_message)

            else:
                self.top_menu.update_lyric_labels(lyrics=self.lyrics)

                self.lyrics_loaded = True

        elif self.current_song.type == "nosong":
            self.top_menu.display_message(message="Open Spotify to start seeing the lyrics!")

        
        elif self.current_song.type == "ad":
            self.top_menu.display_message(message="A Spotify ad is playing")


    def update_current_song(self):
        while True:
            try:
                previous_song_id = self.current_song.id

                raw_data = self.spotify.currently_playing()

                if raw_data == None:
                    self.current_song = NoSongFound()
                else:
                    self.current_song = Song(raw_data=raw_data)

                if not self.current_song.id == previous_song_id:
                    self.song_changed()

            except Exception:
                print(traceback.format_exc())

    def loop(self):

        #Update progress bar
        self.bottom_menu.song_progess_bar.update_progress(self.current_song.progress, self.current_song.length)

        #Hightlight the current lyric
        if self.lyrics_loaded:
            current_lyric = get_timestamp_lyric(lyrics=self.lyrics, timestamp=self.current_song.progress)
            if not current_lyric[0] == self.previous_lyric_index:
                self.top_menu.lyrics_menu.highlight_lyric(index=current_lyric[0])
                self.previous_lyric_index = current_lyric[0]

        self.after(100, self.loop)


class TopMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lyrics_menu = LyricsMenu(master=self, bootstyle=DEFAULT)
        self.messages_menu = MessagesMenu(master=self, bootstyle=DEFAULT)


    def update_lyric_labels(self, lyrics):
        self.lyrics_menu.update_lyric_labels(lyrics=lyrics)
        
        self.messages_menu.pack_forget()
        self.lyrics_menu.pack(expand=YES, fill=BOTH)

        self.bind_all("<Control-MouseWheel>", self.lyrics_menu.on_control_scroll)
    

    def display_message(self, message):
        self.lyrics_menu.pack_forget()
        self.messages_menu.pack(expand=YES, fill=BOTH)

        self.messages_menu.display_message(message=message)

        self.bind_all("<Control-MouseWheel>", self.messages_menu.on_control_scroll)


class MessagesMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_size = 35

        self.label = LyricLabel(master=self, index=-1, lyric="", anchor=CENTER, justify=CENTER, bootstyle=DEFAULT, font=(FONT_BOLD, int(self.font_size*1.5)))
        self.label.pack(side=TOP, fill=BOTH, expand=YES, padx=200)
    
    def display_message(self, message):
        self.label._label.config(text=message)


    def on_control_scroll(self, event):
        delta = event.delta
        
        if delta > 0:
            self.font_size += 2
        if delta < 0:
            self.font_size -= 2
        
        self.font_size = max(6, self.font_size)

        self.label._label.config(font=(FONT_BOLD, int(self.font_size*1.5)))
        

class LyricsMenu(ScrolledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lyric_labels = []
        self.highlighted_lyric_index = -1

        self.font_size = 35

    def update_lyric_labels(self, lyrics):
        #Clear all previous lyric labels
        for label in self.lyric_labels:
            label.destroy()
        self.lyric_labels.clear()

        self.padding_label = LyricLabel(master=self, index=-1, lyric=" \n"*2)
        self.lyric_labels.append(self.padding_label)
        self.padding_label.pack(side=TOP, padx=260, fill=BOTH, expand=YES)

        #Create and pack all the lyric labels
        for i, (timestamp, lyric) in enumerate(lyrics):
            lyric_label = LyricLabel(master=self, index=i, lyric=lyric, font=(FONT_BOLD, self.font_size), anchor=CENTER, justify=CENTER, bootstyle=LIGHT)
            self.lyric_labels.append(lyric_label)
            lyric_label.pack(side=TOP, padx=260, fill=BOTH, expand=YES)


    def highlight_lyric(self, index):
        self.highlighted_lyric_index = index

        for lyric_label in self.lyric_labels:
            if lyric_label.index == index:
                lyric_label._label.config(bootstyle=DEFAULT, font=(FONT_BOLD, int(self.font_size*1.5)))

                self.scroll_to_label(lyric_label)
            else:
                lyric_label._label.config(bootstyle=LIGHT, font=(FONT_BOLD, self.font_size))


    def scroll_to_label(self, label_to_scroll):
        total_height = 0
        for lyric_label in self.lyric_labels:
            total_height += lyric_label.winfo_reqheight()
        
        height_to_scroll = 0
        for lyric_label in self.lyric_labels:
            height_to_scroll += lyric_label.winfo_reqheight()

            if lyric_label is label_to_scroll:
                break
        
        height_to_scroll -= label_to_scroll.winfo_reqheight() // 2
        height_to_scroll -= self.container.winfo_height() // 2

        self.yview_moveto(height_to_scroll/total_height)

    def on_control_scroll(self, event):
        delta = event.delta
        
        if delta > 0:
            self.font_size += 2
        if delta < 0:
            self.font_size -= 2
        
        self.font_size = max(6, self.font_size)

        #Update all the lyric labels
        for lyric_label in self.lyric_labels:
            if lyric_label.index == self.highlighted_lyric_index:
                lyric_label._label.config(font=(FONT_BOLD, int(self.font_size*1.5)))
            else:
                lyric_label._label.config(font=(FONT_BOLD, self.font_size))

class LyricLabel(ttk.Frame):
    def __init__(self, master, index, lyric, *args, **kwargs):
        super().__init__(master=master)
        self.index = index
        self.lyric = lyric

        self._label = WrapLabel(self, text=lyric, *args, **kwargs)
        self._label.pack(fill=BOTH, expand=YES)
        

class BottomMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Configure>", self.on_configure)

        self.grid_columnconfigure(0, weight=25, uniform="xyz")
        self.grid_columnconfigure(1, weight=50, uniform="xyz")
        self.grid_columnconfigure(2, weight=25, uniform="xyz")

        self.song_label = SongLabel(master=self, bootstyle=SECONDARY)
        self.song_label.grid(row=0, column=0, sticky=E+W)

        self.song_progess_bar = SongProgressBar(master=self, bootstyle=SECONDARY)
        self.song_progess_bar.grid(row=0, column=1, sticky=E+W)


    def on_configure(self, event):
        #Update the progress bar length to always be 40% of the window width
        self.song_progess_bar.progress_bar.config(length=int(event.width*0.40))


class SongLabel(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style = ttk.Style()
        self.style.configure("Custom.Transparent.TLabel", background=ttk.Style().colors.secondary)

        self.song_image = ImageTk.PhotoImage(Image.open("assets/default.png").resize((128,128)))
        self.image_lbl = ttk.Label(master=self, image=self.song_image, style="Custom.Transparent.TLabel")
        self.image_lbl.grid(row=0, column=0, rowspan=2, padx=10, pady=5, sticky=W)

        self.song_name_lbl = WrapLabel(master=self, bootstyle=LIGHT, background=ttk.Style().colors.secondary, font=(FONT_LIGHT, 11), anchor=W, justify=LEFT)
        self.song_name_lbl.grid(row=0, column=1, sticky=W+S+E, pady=(10,0))

        self.artist_name_lbl = WrapLabel(master=self, bootstyle=LIGHT, background=ttk.Style().colors.secondary, font=(FONT_LIGHT, 9), anchor=W, justify=LEFT)
        self.artist_name_lbl.grid(row=1, column=1, sticky=W+N+E, pady=(0,10))

        self.columnconfigure(1, weight=1)

    def update_song(self, song:Song):
        self.song_name_lbl.config(text=song.name)
        self.artist_name_lbl.config(text=", ".join(song.artists))

        self.song_image = ImageTk.PhotoImage(song.get_image(edge_radius=60).resize((100, 100)))
        self.image_lbl.config(image=self.song_image)



class SongProgressBar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style = ttk.Style()
        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor=ttk.Style().colors.dark, background=ttk.Style().colors.success, thickness=13)

        self.progress_lbl = ttk.Label(master=self, bootstyle=LIGHT, text="0:00", background=ttk.Style().colors.secondary)
        self.progress_lbl.pack(side=LEFT, padx=8)
        
        self.progress_bar = ttk.Progressbar(master=self, style="Custom.Horizontal.TProgressbar", length=0, value=0)
        self.progress_bar.pack(side=LEFT)

        self.length_lbl = ttk.Label(master=self, bootstyle=LIGHT, text="0:00", background=ttk.Style().colors.secondary)
        self.length_lbl.pack(side=LEFT, padx=8)
    
    def update_progress(self, progress:timedelta, length:timedelta):
        length_seconds = length.total_seconds()
        progress_seconds = min(progress.total_seconds(), length_seconds)

        value = (progress_seconds/length_seconds)*100
        self.progress_bar.config(value=value)

        self.progress_lbl.config(text="{:02}:{:02}".format(int(progress_seconds // 60), int(progress_seconds % 60)))
        self.length_lbl.config(text="{:02}:{:02}".format(int(length_seconds // 60), int(length_seconds % 60)))