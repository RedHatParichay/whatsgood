import tkinter as tk

from AudioClient import AudioClient
from GroupChat.ChatClient import ChatClient
from GroupChat.NicknameDialog import NicknameDialog

class CommOptions(tk.Tk):

    def __init__(self):                         #initialise communication options window
        super().__init__(None)

        self.host = None
        self.title("Lancaster Chatroom")        #set title of main window
        self.geometry("300x100")                #set size of main window
        self.nickname = None                    #set nickname as empty

        #group chat button when clicked will open window to ask for nickname
        self.groupchat_button = tk.Button(self, text="Group chat", command=self.group_chat_clicked)
        self.groupchat_button.pack()

        #audio call button when clicked will
        self.audiocall_button = tk.Button(self, text="Audio call", command=self.audio_call_clicked)
        self.audiocall_button.pack()

    def group_chat_clicked(self):

        self.withdraw()                             #hide main window

        nickname_window = NicknameDialog()          #instantiate nickname dialog window
        #wait for nickname window to be destroyed before continuing
        self.wait_window(nickname_window)

        if nickname_window.nickname:        #if there is a nickname entered in the nickname window
            self.nickname = nickname_window.nickname    #store nickname in this window

            #start new client
            chat_client = ChatClient(self.host, 65432, self.nickname, self.group_chat_closed)
            chat_client.start()

        else:
            self.deiconify()                #show back the CommOptions window

    def group_chat_closed(self):
        self.deiconify()                    #show back the main window
        self.update_idletasks()             #update GUI


    def audio_call_clicked(self):
        self.withdraw()

        audio_client = AudioClient(self.audio_call_closed)
        audio_client.run()

    def audio_call_closed(self):
        self.deiconify()                    #show back the main window
        self.update_idletasks()             #update GUI

    def start(self):
        self.mainloop()                                #start tkinter mainloop

if __name__ == "__main__":
    comm_options = CommOptions()    #instantiate and start communication options window
    comm_options.start()