# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming
# with Software Libraries in Python

# Replace the following placeholders with your information.

# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792

import json
import time
from collections import namedtuple
TIMESTAMP = "1603167689.3928561"
from Profile import Profile

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

def extract_json_dm(json_msg: str) -> MessageTuple:
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


def send_msg(client, token, recipient, message):
    try:
        send = client.makefile('w')
        recv = client.makefile('r')
        msg = {"token": token,
               "directmessage": {"entry": message,
                                 "recipient": recipient,
                                 "timestamp": time.time()}}
        send.write(json.dumps(msg) + '\r\n')
        send.flush()
        resp = recv.readline()
        print('resp: ' + resp)
        if(json.loads(resp))['response']['type'] == 'ok':
            print('ok')
            return True
        else:
            return False
    except Exception as e:
        print('er: ' + str(e))
        return False

def ret_friends(client, token, msgtype, prof):
  send = client.makefile('w')
  recv = client.makefile('r')
  msg = {"token": token, "directmessage": msgtype}
  send.write(json.dumps(msg) + '\r\n')
  send.flush()
  resp = recv.readline()
  tup = extract_json_dm(resp)
  messages = tup.message
  friendL = []
  for item in messages:
    if item['from'] not in friendL:
      friendL.append(item['from'])
  for name in friendL:
    prof.add_friend_list(name)

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

