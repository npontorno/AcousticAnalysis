from tkinter import filedialog
from tkinter import *
import tkinter as tk
import script
from os import listdir
from os.path import isfile, join

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        root.directory = './Results'
        root.resizable(0,0)

    def create_widgets(self):
        self.select_files = tk.Button(self)
        self.select_files["text"] = "Select Files"
        self.select_files["command"] = self.openFiles
        self.select_files.grid(row=1, column=0)

        self.select_dest = tk.Button(self)
        self.select_folder = tk.Button(self)
        
        self.select_folder["text"] = "Select Folder"
        self.select_folder["command"] = self.openFolder
        self.select_folder.grid(row=1, column=2)

        self.or_label = tk.Label(self)
        self.or_label["text"] = "OR"
        self.or_label.grid(row=1, column=1)

        self.file_display = tk.Listbox(self)
        self.file_display["width"] = 122
        self.file_display["height"] = 24
        self.file_display["bg"] = "white"
        self.file_display.grid(row=2, column=0, columnspan=3, rowspan=5, sticky=W+E+N+S, padx=10)

        self.scroll = tk.Scrollbar(self.file_display, orient="vertical")
        self.scroll.config(command=self.file_display.yview)
        self.file_display.config(yscrollcommand=self.scroll.set)
        
        self.select_dest["text"] = "Select Output Destination"
        self.select_dest["command"] = self.selectDest
        self.select_dest.grid(row=10, column=0)

        self.run = tk.Button(self)
        self.run["text"] = "Run"
        self.run["command"] = self.runScript
        self.run.grid(row=10, column=2)

 
    def openFiles(self):
        root.files  =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("WAV files","*.wav"),("all files","*.*")))
        self.file_display.delete(0,END)
        for f in root.files:
            self.file_display.insert(END, f)

    def selectDest(self):
        root.directory = filedialog.askdirectory()

    def openFolder(self):
        root.source = filedialog.askdirectory()
        source_files = [f for f in listdir(root.source) if isfile(join(root.source, f))]
        root.files = []
        for f in source_files:
            root.files.append(root.source + '/' + f)

        self.file_display.delete(0,END)

        for f in root.files:
            self.file_display.insert(END, f)

    def runScript(self):
        print("Running script")
        print("Imported files: ")
        for file in root.files:
            print(file)

        print("Destination Directory" + root.directory)

        script.main(root.files, root.directory)
	
        print("Script Complete")

root = tk.Tk()
root.title("Bird Call Acoustic Analysis")
app = Application(master=root)
root.geometry("1000x500")
app.mainloop()
