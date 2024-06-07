'''
ds_messenger
'''
import json
import ds_client as client
import ds_protocol as protocol

from Profile import Profile


PORT = 3021
HOST = '168.235.86.101'
SEND = 'SENT'
RECV = 'RECV'


class DirectMessage(dict):
    '''
    DirectMessage class that inherits the dictionary class like Profile.
    takes the msgtype, message, timestamp, and sender as parameters.
    every DirectMessage object is a dictionary
    '''
    def __init__(self):
        self.sender = None
        self.message = None
        self.timestamp = None
        self.msg_type = None

    def __init__(self, msg_type, message, timestamp, sender):
        self.set_msg_type(msg_type)
        self.set_message(message)
        self.set_timestamp(timestamp)
        self.set_sender(sender)
        dict.__init__(self,
                      msg_type=self._msg_type,
                      message=self._message,
                      timestamp=self._timestamp,
                      sender=self._sender)

    def set_msg_type(self, msg_type):
        '''
        Sets the message type to either be recv or sent
        '''
        self._msg_type = msg_type
        dict.__setitem__(self, 'msg_type', msg_type)

    def set_message(self, message):
        '''
        Sets the message to what was received
        '''
        self._message = message
        dict.__setitem__(self, 'message', message)

    def set_timestamp(self, timestamp):
        '''
        Sets the timestamp to what was received
        '''
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def set_sender(self, sender):
        '''
        Sets the sender to what was received
        '''
        self._sender = sender
        dict.__setitem__(self, 'sender', sender)

    def get_message(self):
        '''
        gets message
        '''
        return self._message

    def get_timestamp(self):
        '''
        gets timestamp
        '''
        return self._timestamp

    def get_sender(self):
        '''
        gets sender
        '''
        return self._sender

    def get_msg_type(self):
        '''
        gets type of message
        '''
        return self._msg_type
    message = property(get_message, set_message)
    timestamp = property(get_timestamp, set_timestamp)
    sender = property(get_sender, set_sender)
    msg_type = property(get_msg_type, set_msg_type)


class DirectMessenger:
    '''
    DirectMessenger class
    Gets called when users want to
    - send a message
    - retrieve all messages
    - get all friends
    - get messages from a specific sender

    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.socket = client.connect(self.dsuserver)
        self.token = client.join_as_user(self.socket,
                                         self.username,
                                         self.password)
        self.prof = Profile()

    def send(self, message: str, recipient: str) -> bool:
        '''
        Sends a message to the specified recipient
        returns true if message succesfully sent, false if failed
        '''
        msg_send = protocol.send_msg(self.socket,
                                     self.token,
                                     recipient,
                                     message)
        return msg_send

    def retrieve_new(self, prof) -> list:
        '''
        Retrieves all new messages and stores them in a list of
        DirectMessage objects
        Returns the list of DirectMessage objects.
        '''
        new_msg_list = self.recv_dm(self.token, 'new', prof)
        return new_msg_list

    def retrieve_all(self) -> list:
        '''
        Retrieves all messages sent to the user.
        Stores them all in a list of DirectMessage objects
        Returns the list of DirectMessage objects
        '''
        # must return a list of DirectMessage objects containing all messages
        all_msg_list = self.recv_dm(self.token, 'all')
        return all_msg_list

    def get_all_from_friend(self, friend):
        '''
        Retrieves all messeges sent from friend
        Stores in a list of DirectMessage objects
        '''
        all_msg_list = self.recv_dm(self.token, 'all', sender=friend)
        return all_msg_list

    def all_friends(self, prof):
        '''
        Finds the list of all friends that the user has and returns it
        '''
        friend_list = protocol.ret_friends(self.socket,
                                           self.token,
                                           'all', prof)
        return friend_list

    def get_new_from_friend(self, friend, prof):
        '''
        find all new messages from specified friend.
        stores messages in a list of DirectMessage objects
        returns the list.
        '''
        new_msg_list = self.recv_dm(self.token, 'new', prof, friend)
        return new_msg_list

    def recv_dm(self, token, msg_type, prof='', sender=None):
        '''
        Method to reach the server and retrieve direct messages to user.
        paramters will indicate if all or new messages are being retrieved.
        will update the profile if the messages are new
        '''
        send = self.socket.makefile('w')
        recv = self.socket.makefile('r')
        msg = {"token": token, "directmessage": msg_type}
        send.write(json.dumps(msg) + '\r\n')
        send.flush()
        resp = recv.readline()
        tup = protocol.extract_json_dm(resp)
        messages = tup.message
        messagelist = []
        for item in messages:
            dm = DirectMessage(RECV, item['message'], item['timestamp'],
                               item['from'])
            if sender is None or dm.sender == sender:
                messagelist.append(dm)
        messaged_sorted = sorted(messagelist, key=lambda x: x.timestamp)
        if msg_type == 'new':
            for msgs in messaged_sorted:
                prof.add_message_ret(msgs)
        return messaged_sorted
    
def test_messenger():
    # a
    assert True is True
