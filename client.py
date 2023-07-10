from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, \
    messagebox,filedialog
from PIL import ImageTk, Image
import requests
import socket  # Sockets for network connection
import threading  # for multiple process



class GUI:
    client_socket = None
    last_received_message = None

    # Create widgets to initialize GUI
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.exit_button = None
        self.init_socket()
        self.init_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def init_socket(self):
        # initialize the socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = '127.0.0.1'
        server_port = 5000
        # connect to the server
        self.client_socket.connect((server_ip, server_port))


    # intialize the GUI
    def init_gui(self):  # GUI initializer
        self.root.title("COMPUTER NETWORKS SECRET CHAT")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()
        self.display_emoji_buttons()
        self.display_emoji_buttons1()

    # Create a thread to receive messages  continuously
    def listen_for_incoming_messages_in_a_thread(self):
        # Create a thread for sending and receiving at the same time
        thread = threading.Thread(target=self.receive_message,
                                  args=(self.client_socket,))  
        thread.start()

    # Funciton to receive messages
    def receive_message(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')

            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            elif "left the chat" in message:
                print(message)

                self.chat_transcript_area.insert('end', message.split(":")[0] + '\n')
                self.chat_transcript_area.yview(END)
            else:
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)

        so.close()


    def display_emoji_buttons(self):
        frame = Frame()

        emoji_buttons = [
            "😃", "😊", "👍", "👎","🧐", "👻","✋","👌","🦴"  # Add more emojis as needed
        ]
        emoji_x_pos = 490

        for emoji in emoji_buttons:
            button = Button(frame,text=emoji, width=7, command=lambda emoji=emoji: self.on_emoji_button_clicked(emoji))
            button.pack(side='left', padx=(7, 0))
            emoji_x_pos += 30

        frame.pack(side='bottom')
    def display_emoji_buttons1(self):
        frame = Frame()

        emoji_buttons1 = [
             "🎉", "❤️", "😄", "😍","😶", "🙄","😡" ,"😑","☠️"# Add more emojis as needed
        ]
        emoji_x_pos = 490

        for emoji in emoji_buttons1:
            button = Button(frame,text=emoji, width=7, command=lambda emoji=emoji: self.on_emoji_button_clicked(emoji))
            button.pack(side='left', padx=(7, 0))
            emoji_x_pos += 30

        frame.pack(side='bottom')

    def on_emoji_button_clicked(self, emoji):
        self.enter_text_widget.insert('end', emoji)

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter your name:', font=("Arial", 10)).pack(side='left', padx=55)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, font="Arial 10 bold", bg="#ABB2B9", command=self.on_join).pack(side='left',padx=(10, 0))
        self.exit_button = Button(frame, text="Exit", width=10, font="Arial 10 bold", bg="#ABB2B9", command=self.on_close_window).pack(side='left',padx=(10, 10))
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='AGUapp:', font=("Serif", 12)).pack(side='top', anchor='w')
         # Fetch the image from a web URL
        image_url = "https://cdn0.iconfinder.com/data/icons/social-media-with-fill/64/telegram_colour-512.png"  # Replace with your image URL
        response = requests.get(image_url, stream=True)
        image = Image.open(response.raw)
        image = image.resize((150, 150))  # Adjust the size of the image as per your needs

        # Convert the image to Tkinter-compatible format
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        image_label = Label(frame, image=photo)
        image_label.image = photo  # Store a reference to the image to prevent it from being garbage collected
        image_label.pack(side='left', padx=10)

        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Arial", 10)).pack(side='top', anchor='w')

        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', lambda event: self.on_send_button_clicked())
        self.send_button = Button(frame, text="Send", width=10, font="Arial 10 bold", bg="#ABB2B9",command=self.on_send_button_clicked).pack(side='left', padx=(10, 0))

        frame.pack(side='top')

    def on_send_button_clicked(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your name", "Enter your name to send a message")
            return
        self.name_widget.config(state='disabled')
        self.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))


    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()


    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()

        emoji = " 👤 "

        message = (emoji +(senders_name)+ "\n" + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'




    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client_socket.send((self.name_widget.get() + " left the chat").encode('utf-8'))
            self.root.destroy()
            self.client_socket.close()
            exit(0)


# the main function
if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
