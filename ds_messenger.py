
import json
import ds_client as client
import ds_protocol as protocol
import socket
import Profile as profile
import time

PORT = 3021
HOST = '168.235.86.101'

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None



class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
  
    self.socket = client.connect(self.dsuserver)
    self.token = client.join_as_user(self.socket, self.username, self.password)
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      print('here')
      send = self.socket.makefile('w')
      recv = self.socket.makefile('r')
      msg = {"token": self.token, "directmessage": {"entry": message,"recipient": recipient, "timestamp": time.time()}}
      send.write(json.dumps(msg) + '\r\n')
      send.flush()
      resp = recv.readline()
      print(resp)
      if (json.loads(resp))['response']['type'] == 'ok':
        print('ok')
        return True
      else:
        return False
    except Exception as e:
      print('error: ' + str(e))
      return False
    
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    new_msg_list = protocol.ret_msg_only(self.socket, self.token, 'new')
    return new_msg_list
    
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    all_msg_list = protocol.recv_dm(self.socket, self.token, 'all')
    return all_msg_list
  
  def get_all_from_friend(self, friend):
    all_msg_list = protocol.ret_msg_from_sender(self.socket,self.token, friend, 'all')
    return all_msg_list
  
  def get_new_from_friend(self,friend):
    new_msg_list = protocol.ret_msg_from_sender(self.socket,self.token, friend, 'new')
    return new_msg_list

if __name__ == '__main__':
  may = DirectMessenger(HOST, 'may' , 'pwd')
  may.send('YOLO', 'may')
  newList = may.retrieve_new()
  print('List of new:')
  for items in newList:
    print(items)
  print('List of all:')
  allList = may.retrieve_all()
  for items in allList:
    print(items)
  