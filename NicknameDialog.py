import tkinter as tk

class NicknameDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Nickname Input")        #set title of dialog window
        self.geometry("300x125")            #set size of dialog window

        self.label = tk.Label(self, text="Enter your nickname:")    #print label
        self.label.pack(pady=5)

        self.nickname_entry = tk.Entry(self)               #create area to enter nickname
        self.nickname_entry.pack(pady=10)

        #create ok button to receive nickname
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack()

        self.nickname = None                #set nickname as empty

    def on_ok(self):                    #when ok button clicked
        self.nickname = self.nickname_entry.get()       #get entered nickname
        self.destroy()                                  #destroy window

    def start(self):
        self.mainloop()                                 #start tkinter mainloop

if __name__ == "__main__":                              #run nickname dialog window
    root = tk.Tk()
    nickname_dialog = NicknameDialog()
    nickname_dialog.start()