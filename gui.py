from tkinter import *
import tkinter.filedialog as tkFileDialog
import excrypt
import winsound
import os


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.parent.title("ExCrypt v0.1")
        self.pack(fill=BOTH, expand=1)
        self.center_window()
        #root.geometry("250x250+300+300")
        
        encrypt_button = Button(self, text="Encrypt dir", command=self.encrypt_file, width=10)
        encrypt_button.grid(row=0, column=0)
        
        decrypt_button = Button(self, text="Decrypt dir", command=self.decrypt_file, width=10)
        decrypt_button.grid(row=1, column=0)
        
        #browse_button = Button(self, text="Browse", command=self.askopenfilename, width=10)
        #browse_button.grid(row=0, column=0)
        

    def center_window(self):
        w, h = 250, 100
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)//2
        y = (sh - h)//2
        
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))
        
    def encrypt_file(self):
        source_path = tkFileDialog.askdirectory()
        key = "hi"  # Until create popup window
        excrypt.AES_dir_encrypt(source_path, key)
        print("Encrypted")
        
    def decrypt_file(self):
        source_path = tkFileDialog.askopenfilename()
        key = "hi"
        excrypt.AES_dir_decrypt(source_path, key)
        print("Decrypted")

def main(): 
    root = Tk()
    app = Window(root)
    root.mainloop()

main()
