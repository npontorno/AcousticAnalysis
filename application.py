from tkinter import filedialog
from tkinter import *
import tkinter as tk
import script

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.select_files = tk.Button(self)
        self.select_files["text"] = "Select Files"
        self.select_files["command"] = self.openFiles
        self.select_files.grid(row=8, column=1)

        self.select_dest = tk.Button(self)
        self.select_dest["text"] = "Select Output Destination"
        self.select_dest["command"] = self.selectDest
        self.select_dest.grid(row=10, column=1)

        self.run = tk.Button(self)
        self.run["text"] = "Run"
        self.run["command"] = self.runScript
        self.run.grid(row=12, column=1)


    def openFiles(self):
        root.files  =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("WAV files","*.wav"),("all files","*.*")))
        

    def selectDest(self):
        root.directory = filedialog.askdirectory()

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
root.geometry("500x500")
app.mainloop()
