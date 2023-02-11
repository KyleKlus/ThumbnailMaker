import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import image_manager as imang


class Window:
    def __init__(self, name, version):
        self.__STANDARD_COVER_SIZE = 600
        # config window
        self.window = tk.Tk()
        self.window.title(name + " - v" + version)
        self.window.geometry("300x150")
        self.window.resizable(0, 0)
        self.window.config(bg = "black")
        
        # config top frame
        self.top_f = tk.Frame(master = self.window, 
                            relief = tk.FLAT, 
                            borderwidth = 1, 
                            width = 165, height = 46, bg = "black")
        self.top_f.pack()
        
        # config size lable
        self.info_size_lbl = tk.Label(master = self.top_f, 
                                    text = "Cover size (px):", 
                                    bg = "black", fg = "white")
        self.info_size_lbl.place(x = 0, y = 20, width = 110, height = 25)
        
        # config size entrybox
        self.size_entry = tk.Entry(master = self.top_f, relief = tk.SOLID, borderwidth = 1)
        self.size_entry.insert(0, self.__STANDARD_COVER_SIZE)
        self.size_entry.place(x = 110, y = 20, width = 40, height = 25)
        
        # config mode checkbutton
        self.mode = tk.IntVar()
        self.del_c_btn = tk.Checkbutton(master = self.window, 
                                            text = 'Delete after processing', 
                                            variable = self.mode,
                                            fg = "white", bg = "black",
                                            activebackground="black", 
                                            activeforeground="white", 
                                            selectcolor="grey")
        self.del_c_btn.deselect()
        self.del_c_btn.pack()
        
        # config progressbar
        self.progress = ttk.Progressbar(self.window, 
                                        orient = tk.HORIZONTAL, 
                                        length = 200, mode = 'determinate')
        
        # config startbutton
        self.start_btn = tk.Button(self.window, 
                                text = "Select & Start", 
                                width = 10, command = self.btn_akt_start)
        self.start_btn.pack()
        

    
    def start(self):
        self.window.mainloop() # starts the initialized window
        
    
    
    def btn_akt_start(self): # called when startbutton is pressed
        # Open fileselectiondialog
        path = tk.filedialog.askopenfilenames(title = "Select files",
                                            filetypes = (("JPEG files", "*.jpg"), ("all files", "*.*")))
        
        total = len(path) # total number of files to be processed
        done = 0
        
        if total != 0:
            # initiate the progressbar
            self.progress['maximum'] = total
            self.progress['value'] = done
            self.progress.pack()
            self.window.update_idletasks()
            
            self.del_c_btn.config(state = "disabled")
            
            for infile in path:
                file, ext = os.path.splitext(infile) # get the current filepath
                if ext == ".jpg":
                    if self.mode.get() == 1:
                        datatype = ".jpg"
                    elif self.mode.get() == 0:
                        datatype = " Cover.jpg"
                
                    imang.generate_cover(infile, int(self.size_entry.get())).save(file + datatype, "JPEG")
                
                    # update the progressbar
                    done += 1
                    self.progress['value'] = done
                    self.window.update_idletasks()
                
            
            self.progress.pack_forget() # reset the progressbar
            self.del_c_btn.config(state = "normal")

