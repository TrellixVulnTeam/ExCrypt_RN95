from tkinter import *
import tkinter.filedialog as tkFileDialog
import excrypt
import winsound
import os

__version__ = "0.2.1"


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.parent.title("ExCrypt v" + __version__)
        self.pack(fill=BOTH, expand=1)
        self.center_window()
        
        encryptButton = Button(self, text="Encrypt dir", command=self.encrypt_file, width=10)
        encryptButton.grid(row=0, column=2, padx=5, pady=2)
        
        decryptButton = Button(self, text="Decrypt dir", command=self.decrypt_file, width=10)
        decryptButton.grid(row=1, column=2, padx=5)
        
        entryField = Entry(self, width=20)
        entryField.grid(row=0, column=1)
        self.key = entryField.get()

        keyText = Label(self, text="Key: ").grid(row=0, column=0)

        musicButton = Button(self,  text="Play music", command=self.play_music)
        musicButton.grid(row=1, column=1)


    def center_window(self):
        w, h = 250, 70
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)//2
        y = (sh - h)//2
        
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))
        
    def encrypt_file(self):
        source_path = tkFileDialog.askdirectory()
        print(source_path)
        excrypt.AES_dir_encrypt(source_path, self.key)
        print("Encrypted")
        
    def decrypt_file(self):
        source_path = tkFileDialog.askopenfilename()
        print(source_path)
        excrypt.AES_dir_decrypt(source_path, self.key)
        print("Decrypted")

    def play_music(self):
        winsound.PlaySound("amstrad_memories.wav", winsound.SND_LOOP | winsound.SND_ASYNC)
        

def main(): 
    root = Tk()

    root.resizable(0,0)
    root.iconbitmap(r'lock-yellow.ico')

    app = Window(root)
    root.mainloop()

main()
