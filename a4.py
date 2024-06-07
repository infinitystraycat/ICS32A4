'''
This is the gui code which will control all of the UI aspects.
The a4.py will call the main function of this code.
'''
import time
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from Profile import Profile
import ds_client as client
from ds_messenger import DirectMessenger


HOST = '168.235.86.101'


class Body(tk.Frame):
    '''
    This is the Body class for the body section of the UI.
    '''
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        '''
        Handles the node selection when the contact is clicked
        '''
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        print('node select: ' + str(entry))
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        '''
        Method to allow contact to be added to the contacts node
        '''
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, cont_id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        cont_id = self.posts_tree.insert('', cont_id, cont_id, text=contact)

    def insert_user_message(self, message: str):
        '''
        Displays message sent by the user on the right side of the screen
        '''
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        '''
        Displays message sent by the person you are messaging,
        on the left side of the screen
        '''
        self.entry_editor.insert(tk.END, str(message) + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        '''
        gets the text message information entered by the user
        '''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''
        sets the text message in the entry box
        currently is unused
        '''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''
    Class handling method inside the "footer"
    Includes the send button
    '''
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''
        Method that is tied to the send button,
        Will help set the callback message.
        '''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class ProfileDialog(tk.simpledialog.Dialog):
    '''
    Class to display a textbox for user to enter
    the file path of the profile they want to load.
    Requires the whole dsu file.
    '''
    def __init__(self, root, title=None, path=None):
        self.path = path
        super().__init__(root, title)

    def body(self, frame):
        self.path_label = tk.Label(frame, width=30, text="Profile Path")
        self.path_label.pack()
        self.path_entry = tk.Entry(frame, width=30)
        self.path_entry.pack()

    def apply(self):
        self.path = self.path_entry.get()


class LoginDialog(tk.simpledialog.Dialog):
    '''
    Class to display a textbox for user to enter
    server and login details of the user they
    want to connect to.
    '''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.server = server
        self.user = user
        self.pwd = pwd
        # self.title = title
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.pwd_label = tk.Label(frame, width=30, text="Password")
        self.pwd_label.pack()
        self.pwd_entry = tk.Entry(frame, width=30, show="*")
        self.pwd_entry.pack()
        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.pwd_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    '''
    The main class for the app.
    '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.path = None
        self.profile = None
        self.online = False
        self.first_time = True
       
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = ... continue!
        # TODO
        findp = ProfileDialog(self.root, "Load Profile", self.path)
        self.path = findp.path
        self.profile = Profile()
        open_p = Path(self.path)
        
        is_connect = self.configure_server()
        if not open_p.exists():
            file = open(self.path, 'w', encoding="utf-8")
            file.close()
            prof = Profile(self.server, self.username, self.password)
            prof.save_profile(self.path)
            self.profile.load_profile(self.path)
        else:
            self.profile.load_profile(self.path)

        self._draw()

        if not is_connect:
            self.online = False
            friends = self.profile.get_friend_list()
            for names in friends:
                self.body.insert_contact(names)
        else:
            self.online = True
            # self.body.insert_contact("studentexw23")  # adding one ex student.
            contacts = self.direct_messenger.all_friends(self.profile)
            for name in contacts:
                self.profile.add_friend_list(name)
            print('contact:  ' + str(contacts))
            self.profile.save_profile(self.path)
            for names in contacts:
                self.body.insert_contact(names)
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
        print('a')
        #if self.first_time is False:
        #self.after(2000, self.check_new)
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        
    def send_message(self):
        '''
        Method that takes care of sending messages
        Will display error message if offline
        '''
        # You must implement this!
        if not self.online:
            tk.messagebox.showinfo("Send Error", "Offline mode"
                                   " - Can't send message")
            return
        message = self.body.get_text_entry()
        self.body.insert_user_message(message)
        self.direct_messenger.send(message, self.recipient)
        mess = {"msg_type": "SENT", "message": message,
                "recipient": self.recipient, "timestamp": time.time()}
        self.profile.add_to_sent_messages(mess)
        self.profile.save_profile(self.path)
        self.body.message_editor.delete(1.0, tk.END)

    def add_contact(self):
        '''
        Method to add a contact to the node.
        Will give an error message if in offline mode.
        '''
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        if not self.online:
            tk.messagebox.showinfo("Send Error",
                                   "Offline mode - Can't add contact")
            return
        
        add_contact = tk.simpledialog.askstring(title="Add Contact",
                                                prompt="Enter the name of "
                                                "the contact you want to add")
        self.body.insert_contact(add_contact)
        print('contact:  ' + str(add_contact))
        self.profile.add_friend_list(add_contact)

    def recipient_selected(self, recipient):
        '''
        function to handle recipient selection.
        When sender is selected on tree:
            - displays the messages sent to them and received
        Will grab messages stored in profile if offline
        '''
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        if self.online:
            recv_messages = self.direct_messenger.get_all_from_friend(self.recipient)
        elif not self.online:
            recv_messages = self.profile.get_recv_messages_recipient(self.recipient)

        sent_messages = self.profile.get_sent_messages_recipient(self.recipient)

        print('here are ret sent messages: ' + str(sent_messages))
        combined = recv_messages + sent_messages
        for item in combined:
            print(item)
            item['timestamp'] = str(item['timestamp'])
        sort_comb = sorted(combined, key=lambda x: x['timestamp'])
        #sort_comb = list(dict.fromkeys(sort_comb))
        for message in sort_comb:
            print(message)
            if message["msg_type"] == "RECV":
                print('ha')
                self.body.insert_contact_message(message["message"])
            else:
                self.body.insert_user_message(message["message"])
        if self.first_time is True:
            self.after(2000, self.check_new)
            self.first_time = False
    # print(id)

    def configure_server(self):
        '''
        Method to attempt to connect to the server
        If can't connect (offline), returns false
        If it can connect, returns true, and sets the direct_mess

        '''
        ud = LoginDialog(self.root, "Configure Account",
                         self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        print('suer!')
        print(self.username)
        can_connect = client.connect(self.server)
        if not can_connect:
            self.online = False
            return False
        if can_connect:
            self.online = True
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
            return True
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

    # publish is not necessary
    def publish(self, message: str):
        '''
        not using this method
        '''
        # You must implement this!

    def check_new(self):
        '''
        Constantly checks for new messages and new contacts
        only runs if online
        '''
        # You must implement this!and self.first_time is False
        if self.online:
            friends = self.direct_messenger.all_friends(self.profile)
            orig_list = self.profile.get_friend_list()
            for friend in friends:
                if friend not in orig_list:
                    self.body.insert_contact(friend)
            new_messages = self.direct_messenger.get_new_from_friend(self.recipient,
                                                                     self.profile)
            if new_messages:
                for message in new_messages:
                    print('wah')
                    self.body.insert_contact_message(message["message"])
                    #message_tup = {"msg_type": 'RECV',
                    #               "message": message,
                    #               "recipient": self.recipient,
                    #              "timestamp": time.time()}
                    #self.profile.add_message_ret(message_tup)
        self.after(2000, self.check_new)
        # print('here now')
        # self.first_time = False

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()
    #profname = tk.simpledialog.askstring('get pofile dialog','profile path:') 
    
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # id = main.after(2000, app.check_new)
    # print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    app.update()
    main.mainloop()
    #id = main.after(2000, app.check_new)
    # print(id)
