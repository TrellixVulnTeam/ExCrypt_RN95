from tkinter import *
import tkinter.filedialog as tkFileDialog
import excrypt
import winsound
import os

__version__ = "0.3"


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.parent.title("ExCrypt v" + __version__)
        self.pack(fill=BOTH, expand=1)
        self.center_window()
        
        encryptDirButton = Button(self, text="Encrypt dir", command=self.encrypt_dir, width=12)
        encryptDirButton.grid(row=0, column=2, padx=5, pady=2)

        encryptFileButton = Button(self, text="Encrypt file", command=self.encrypt_file, width=12)
        encryptFileButton.grid(row=1, column=2, padx=5)
        
        decryptButton = Button(self, text="Decrypt dir/file", command=self.decrypt_file, width=12)
        decryptButton.grid(row=2, column=2, padx=5)
        
        self.entryField = Entry(self, width=20)
        self.entryField.grid(row=0, column=1)

        keyText = Label(self, text="Key: ").grid(row=0, column=0)

        musicButton = Button(self,  text="Play music", command=self.play_music)
        musicButton.grid(row=2, column=1)


    def center_window(self):
        w, h = 260, 90
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)//2
        y = (sh - h)//2
        
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))


    def encrypt_dir(self):
        source_path = tkFileDialog.askdirectory()
        print(source_path)
        self.get_entry()
        excrypt.AES_dir_encrypt(source_path, self.key)

        print("Encrypted dir")


    def encrypt_file(self):
        source_path = tkFileDialog.askopenfilename()
        print(source_path)
        self.get_entry()
        excrypt.AES_dir_encrypt(source_path, self.key)

        print("Encrypted file")

        
    def decrypt_file(self):
        source_path = tkFileDialog.askopenfilename()
        print(source_path)
        self.get_entry()
        excrypt.AES_dir_decrypt(source_path, self.key)

        print("Decrypted")


    def play_music(self):
        winsound.PlaySound("amstrad_memories.wav", winsound.SND_LOOP | winsound.SND_ASYNC)


    def get_entry(self):
        self.key = self.entryField.get()
        if not self.key:
            print("No key entered!")
        

def main(): 
    root = Tk()

    root.resizable(0,0)
    root.iconbitmap(r'lock-yellow.ico')

    app = Window(root)
    root.mainloop()

main()
