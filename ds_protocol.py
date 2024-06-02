# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming
# with Software Libraries in Python

# Replace the following placeholders with your information.

# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792

import json
from collections import namedtuple
TIMESTAMP = "1603167689.3928561"

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ["type", "message", "token"])


def extract_json(json_msg: str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert
  it to a DataTuple object
  TODO: replace the pseudo placeholder keys with actual
  DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj["response"]['type']
    message = json_obj["response"]["message"]
    if str(type) == 'error':
      print('Error: ' + str(message))
    token = json_obj["response"]["token"]
  except json.JSONDecodeError as e:
    if str(type) == 'error':
      print('Error: ' + str(message))
    print("Json cannot be decoded.")
    print(e)
  return DataTuple(type, message, token)

MessageTuple = namedtuple('MessageTuple', ["type", "message"])
def extract_json_dm(json_msg: str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert
  it to a DataTuple object
  TODO: replace the pseudo placeholder keys with actual
  DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj["response"]['type']
    message = json_obj["response"]["messages"]
    if str(type) == 'error':
      print('Error: ' + str(message))
  except json.JSONDecodeError as e:
    if str(type) == 'error':
      print('Error: ' + str(message))
    print("Json cannot be decoded.")
    print(e)
  return MessageTuple(type, message)


def send_msg(client, token, recipient, message ):
  try:
    send = client.makefile('w')
    recv = client.makefile('r')
    msg = {"token": token, "directmessage": {"entry": message,"recipient": recipient, "timestamp": "1603167689.3928561"}}
    send.write(json.dumps(msg) + '\r\n')
    send.flush()
    resp = recv.readline()
    print('resp: ' + resp)
  except Exception as e:
    print('er: ' + str(e))

def recv_dm(client, token, type):
  send = client.makefile('w')
  recv = client.makefile('r')
  msg = {"token": token, "directmessage": type}
  send.write(json.dumps(msg) + '\r\n')
  send.flush()
  resp = recv.readline()
  tup = extract_json_dm(resp)
  messages = tup.message
  messageD = {}
  messageL = []
  for item in messages:
    #print(item)
    print(item)
    mess = 'Message: ' + item['message'] + ' From: ' + item['from'] 
    messageD[item['timestamp']] = mess
    messageL.append(mess)

  sortedL = sorted(messageD.items(),key=lambda item: item[1], reverse=True)
  return sortedL
  #if tup.type == 'ok':
    #print(tup)

def ret_friends(client, token, type):
  send = client.makefile('w')
  recv = client.makefile('r')
  msg = {"token": token, "directmessage": type}
  send.write(json.dumps(msg) + '\r\n')
  send.flush()
  resp = recv.readline()
  tup = extract_json_dm(resp)
  messages = tup.message
  friendL = []
  for item in messages:
    #print(item)
    friendL.append(item['from'])
  return friendL

def ret_msg_only(client, token, type):
  send = client.makefile('w')
  recv = client.makefile('r')
  msg = {"token": token, "directmessage": type}
  send.write(json.dumps(msg) + '\r\n')
  send.flush()
  resp = recv.readline()
  tup = extract_json_dm(resp)
  messages = tup.message
  msgL = []
  for item in messages:
    #print(item)
    msgL.append(item['message'])
  return msgL

def ret_msg_from_sender(client, token, sender, type):
  send = client.makefile('w')
  recv = client.makefile('r')
  msg = {"token": token, "directmessage": type}
  send.write(json.dumps(msg) + '\r\n')
  send.flush()
  resp = recv.readline()
  tup = extract_json_dm(resp)
  messages = tup.message
  messageL = []
  for message in messages:
    if message['from'] == sender:
      messageL.append(message['message'])
  return messageL