import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DTXT")
        self.overrideredirect(True)
        self.configure(bg="#3d3d3d")
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#3d3d3d")
        self.style.configure("TLabel", background="#3d3d3d", foreground="white")
        self.style.configure("TButton", background="white", foreground="black")       
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = screen_width // 2
        height = screen_height // 2
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")  # set window size and position
        self.bind("<Button-2>", self.start_drag)
        self.bind("<B2-Motion>", self.on_drag)
        self.bind("<Button-3>", self.start_resize)
        self.bind("<B3-Motion>", self.on_resize)
        button_height = 30
        self.header = ttk.Frame(self, style="TFrame", height=button_height)
        self.header.pack(side=tk.TOP)
        button1 = ttk.Button(
            self.header, text="OPEN", command=self.open_file)
        button1.pack(fill=tk.X, expand=True, side=tk.LEFT)
        button2 = ttk.Button(
            self.header, text="SAVE", command=self.save_file)
        button2.pack(fill=tk.X, side=tk.LEFT, expand=True)
        button3 = ttk.Button(
            self.header, text="VOICE", command=self.activate_voice_recognition)
        button3.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.bottom = ttk.Frame(self, style="TFrame", height=button_height)
        self.bottom.pack(side=tk.BOTTOM)
        button4 = ttk.Button(
            self.bottom, text="CLOSE", command=self.destroy)
        button4.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.content = ttk.Frame(self, style="TFrame")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text_editor = tk.Text(self.content, bg="black", fg="green")
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    def activate_voice_recognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en-US')
            print("Transcripción: " + text)
            self.text_editor.insert(tk.END, text + " ")
        except sr.UnknownValueError:            
            self.content_label.config(text="Audio could not be recognized")            
        except sr.RequestError as e:            
            self.content_label.config(text="Error requesting results from the speech recognition service")
    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, "r") as f:
                self.text_editor.delete("1.0", tk.END) # clear the text editor
                self.text_editor.insert(tk.END, f.read())
    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            with open(filepath, "w") as f:
                f.write(self.text_editor.get("1.0", tk.END))           
    def start_resize(self, event):
        self._resizing = True
        self._x = event.x_root
        self._y = event.y_root
        self._width = self.winfo_width()
        self._height = self.winfo_height()
    def on_resize(self, event):
        if self._resizing:
            width = max(100, self._width + event.x_root - self._x)
            height = max(100, self._height + event.y_root - self._y)
            self.geometry(f"{width}x{height}")   
    def start_drag(self, event):
        self._dragging = True
        self._x = event.x
        self._y = event.y
    def on_drag(self, event):
        if self._dragging:
            x = self.winfo_x() + (event.x - self._x)
            y = self.winfo_y() + (event.y - self._y)
            self.geometry(f"+{x}+{y}")
    def destroy(self):
        self._dragging = False
        super().destroy()

disk_usage = GUI()
disk_usage.mainloop()
