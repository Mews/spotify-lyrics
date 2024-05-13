from gui import MainUi
import settings

ui = MainUi(title="Spotify Lyrics Client", themename=settings.theme)

ui.geometry("1100x700")
ui.minsize(825, 575)
ui.iconbitmap("assets/icon.ico")

ui.mainloop()