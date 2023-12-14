# client.py
import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label

class ChatApp(App):
    def __init__(self, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""
        self.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0","#808080","#800000","#808000","#008000","#800080","#008080","#000080","#FFA500","#800080"]
        self.message_colors = {}

    def build(self):
        self.create_interface()
        self.show_username_popup()
        threading.Thread(target=self.connect_server).start()
        return self.root



    def create_interface(self):
        self.root = BoxLayout(orientation="vertical")

        #  create box layout to Label for received messages
        boxchat = BoxLayout(orientation="vertical", size_hint_y=None, height=500)
        self.message_box = Label(font_size=14, markup=True, text="")
        boxchat.add_widget(self.message_box)
        self.root.add_widget(boxchat)



        # Box for message input and send button
        input_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)

        # Text input for sending messages
        self.text_input = TextInput(font_size=14)
        input_box.add_widget(self.text_input)

        # Send button
        self.send_button = Button(text="Send", size_hint_x=None, width=100)
        self.send_button.bind(on_press=self.send_message)

        input_box.add_widget(self.send_button)
        self.root.add_widget(input_box)


    def show_username_popup(self):
        content = BoxLayout(orientation="vertical")
        username_input = TextInput(hint_text="Enter your username", multiline=False)
        content.add_widget(username_input)

        popup = Popup(title='Username Input', content=content, size_hint=(None, None), size=(300, 200),
                      auto_dismiss=False)
        
        def set_username(instance):
            self.username = username_input.text
            popup.dismiss()

        ok_button = Button(text='OK', size_hint_y=None, height=50)
        ok_button.bind(on_press=set_username)
        content.add_widget(ok_button)

        popup.open()

    def send_message(self, instance):
        # if message is empty, don't send anything

        if not self.username:
            self.show_username_popup()
        elif not self.text_input.text:
            return
        else:
            message = f"{self.username}: {self.text_input.text}\n"
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.text_input.text = ""
            except BrokenPipeError:
                print("Error: The server has closed the connection.")
                self.client_socket.close()
                self.connect_server()

    def connect_server(self):
        try:
            self.client_socket.connect(('10.112.40.222', 5555))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print(f"Error connecting to the server: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                Clock.schedule_once(lambda dt: self.update_message_box(message))
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def get_user_color(self, username):
        if username not in self.message_colors:
            # Assign a color to the username if it's not already assigned
            color_index = len(self.message_colors) % len(self.colors)
            self.message_colors[username] = self.colors[color_index]

        return self.message_colors[username]
    
    def update_message_box(self, message):
        username, content = message.split(":", 1)
        myuser ,content = content.split(":", 1)

        color = self.get_user_color(username)
        # conent with white color
        formatted_message = f"[color={color}]{myuser}[/color]:[color=#FFFFFF]{content}[/color]\n"
        self.message_box.text += formatted_message

if __name__ == "__main__":
    ChatApp().run()
