from tkinter import Event
from ttkbootstrap import Label

class WrapLabel(Label):
    """A label that automatically wraps its text when resized.
    When using this label, the geometry manager must be configured
    to resize the widget in some way, otherwise the width will
    default to the text's max length.
    This can mean using ``.pack(fill="both", expand=True)``, or
    ``.place(relwidth=1, relheight=1)``, or by configuring grid
    weights appropriately.
    ``minwidth=`` can be specified to prevent wrapping under
    a certain width which can significantly improve performance
    for longer lines of text.
    """
    #Taken from https://gist.github.com/thegamecracks/5595dad631ec50bdc021f945054e86fb

    def __init__(self, *args, minwidth: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.minwidth = minwidth
        self.bind("<Configure>", self.__on_configure)

    def __on_configure(self, event: Event):
        width = max(self.minwidth, self.__get_width())
        if width != 1:  # Prevent wrapping on initial configuration
            self.configure(wraplength=width)

    def __get_width(self) -> int:
        if self.winfo_manager() == "grid":
            # Wrap to the bounding box reserved for the label
            # instead of the container's full width.
            # Not doing this might lead to clipped text.
            options = self.grid_info()
            bbox = self.master.grid_bbox(options["column"], options["row"])
            if bbox is None:
                return 1

            width = bbox[2]
            if isinstance(options["padx"], int):
                padx = options["padx"] * 2
            else:
                padx = sum(options["padx"])

            return width - padx
        else:
            return self.master.winfo_width()