import json

from screeninfo import get_monitors, Monitor
import tkinter as tk
import tkinter.ttk as ttk
from HandTracking.Camera import Camera
from HandTracking.ConfigHandler import ConfigHandler


class Settings:
    def __init__(self, monitor: Monitor = Monitor(width=640, height=360, x=0, y=0), fullscreen: int = 1,
                 camera: int = 0) -> None:
        self.monitor: Monitor = monitor
        self.is_fullscreen: int = fullscreen
        self.camera: int = camera

    @classmethod
    def from_dict(cls, dictionary: dict) -> 'Settings':
        """
        Overload of the constructor, which creates a Settings object from a dictionary.

        :param dictionary: The dictionary to extract attributes from
        :return: A Settings object containing the attributes defined in the dictionary
        """
        monitor: Monitor = Monitor(width=dictionary["monitor"]["width"],
                                   height=dictionary["monitor"]["height"],
                                   x=dictionary["monitor"]["x"],
                                   y=dictionary["monitor"]["y"])

        return Settings(monitor, dictionary["is_fullscreen"], dictionary["camera"])

    def to_dict(self) -> dict:
        """
        Converts the Settings object to a dictionary representation.

        :return: A dictionary resembling the Settings object
        """

        string: str = json.dumps(self, default=lambda o: o.__dict__)
        dictionary: dict = json.loads(string)

        return dictionary


class SettingsApp:
    def __init__(self, master=None) -> None:
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.appliedSettings = Settings()
        # radio button stuff
        self.radioVar = tk.StringVar()  # used to get the 'value' property of a tkinter.Radiobutton
        self.radioVar.set(True)

        self.labelframe1 = ttk.Labelframe(self.toplevel1)
        self.fullscreen = ttk.Radiobutton(self.labelframe1)
        self.fullscreen.configure(text='Fullscreen', variable=self.radioVar, value=True)
        self.fullscreen.pack(anchor='w', side='top')
        self.windowed = ttk.Radiobutton(self.labelframe1)
        self.windowed.configure(text='Window', variable=self.radioVar, value=False)
        self.windowed.pack(anchor='w', side='top')
        self.labelframe1.configure(height='200', text='Window mode', width='200')
        self.labelframe1.pack(anchor='nw', ipadx='10', ipady='10', padx='10', pady='10', side='top')

        # monitor stuff
        self.label1 = ttk.Label(self.toplevel1)
        self.label1.configure(text='Monitor')
        self.label1.pack(anchor='w', padx='10', side='top')
        self.selected_monitor = tk.StringVar()
        self.Monitorbox = ttk.Combobox(self.toplevel1, textvariable=self.selected_monitor)
        self.Monitorbox.pack(anchor='w', padx='10', side='top')
        self.monitor_list = {}
        for idx, m in enumerate(get_monitors()):
            self.monitor_list["Display{num}".format(num=idx + 1)] = m
        self.Monitorbox['values'] = list(self.monitor_list.keys())
        self.Monitorbox.current(0)
        self.Monitorbox['state'] = 'readonly'

        # webcam stuff
        self.active_cams = Camera.return_camera_indexes()
        self.selected_cam = tk.StringVar()

        self.label2 = ttk.Label(self.toplevel1)
        self.label2.configure(text='Webcam')
        self.label2.pack(anchor='w', padx='10', side='top')
        self.Webcambox = ttk.Combobox(self.toplevel1, textvariable=self.selected_cam)
        self.Webcambox.pack(anchor='w', padx='10', side='top')
        self.Webcambox['values'] = self.active_cams
        self.Webcambox.current(0)
        self.Webcambox['state'] = 'readonly'

        # cancel button stuff
        self.Cancel = ttk.Button(self.toplevel1)
        self.Cancel.configure(text='Cancel')
        self.Cancel.pack(anchor='se', padx='10', pady='10', side='right')
        self.Cancel.configure(command=self.cancel)

        # ok button stuff
        self.OK = ttk.Button(self.toplevel1)
        self.OK.configure(text='OK')
        self.OK.pack(anchor='se', padx='10', pady='10', side='right')
        self.OK.configure(command=self.save)

        # main widget stuff
        self.toplevel1.configure(borderwidth='2', height='200', width='200')
        self.toplevel1.geometry('352x352')
        self.toplevel1.title('Settings')

        # Main widget
        self.mainwindow = self.toplevel1

    def run(self) -> Settings:
        """
        Starts the settings window's loop.
        :return:
        """
        self.mainwindow.mainloop()

        return self.appliedSettings

    # TODO: make it destroy everything
    def cancel(self) -> None:
        """
        Closes the settings window.
        """
        self.toplevel1.destroy()

    def save(self) -> None:
        """
        Saves the chosen values in memory as well as calling the writing to a config file.
        """
        self.appliedSettings.monitor = self.monitor_list[self.selected_monitor.get()]
        self.appliedSettings.is_fullscreen = int(self.radioVar.get())
        self.appliedSettings.camera = int(self.selected_cam.get())
        if int(self.radioVar.get()) == 0:
            self.appliedSettings.monitor.width = 640
            self.appliedSettings.monitor.height = 360

        ConfigHandler.save_startup_settings(self.appliedSettings.to_dict())

        self.toplevel1.destroy()


def run_settings() -> Settings:
    """
    Initializes the settings app and runs it.
    """
    app = SettingsApp()
    return app.run()
