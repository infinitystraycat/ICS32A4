# Starter code for assignment 3 in ICS 32 Programming with
# Software Libraries in Python

# Replace the following placeholders with your information.

# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792
import socket
import threading
import ds_protocol as protocol
import json
# import requests

PORT = 3021
HOST = '168.235.86.101'
TIMESTAMP = "1603167689.3928561"


def send(server: str, port: int, username: str, password: str,
         message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    # Additional code notes
    '''
    - Will display an error if post or bio is blank
    - This gets overturned if only uploading bio
    - The way the code uploads just the bio is:
      'nopost' is passed in as the message.

    '''
    # TODO: return either True or False depending on
    # results of required operation
    try:
        if len(message.strip()) < 1:
            print('ERROR: You can not upload a blank post')
            return False
        if bio:
            if len(bio.strip()) < 1:
                print('ERROR: You can not upload a blank bio')
                return False

        client = connect(server)
        send = client.makefile('w')
        recv = client.makefile('r')

        token = join_as_user(client, username, password)
        if message.strip().lower() == 'nopost' and bio:
            cbio = {"token": token, "bio":
                   {"entry": bio, "timestamp": TIMESTAMP}}
            send.write(json.dumps(cbio) + '\r\n')
            send.flush()
            resp = recv.readline()
            print('resp: ' + resp)
        else:
            post = {"token": token, "post": {"entry": message,
                                             "timestamp": TIMESTAMP}}
            send.write(json.dumps(post) + '\r\n')
            send.flush()
            resp = recv.readline()
            print('resp: ' + resp)
            if bio:
                cbio = {"token": token, "bio": {"entry": bio,
                                                "timestamp": TIMESTAMP}}
                send.write(json.dumps(cbio) + '\r\n')
                send.flush()
                resp = recv.readline()
                print('resp: ' + resp)
        client.close()
        return True
    except Exception as e:
        print('Error as: ' + str(e))
        print('No proper input given. Please check your inputs.')
        return False
    



def join_as_user(client, usr, pwd):
    '''
    Logs in using the provided username and password,
    and returns a token.
    '''
    join_msg = {"join": {"username": usr, "password": pwd, "token": ""}}
    #{"join": {"username": ohhimark, "password": password, "token": ""}}

    send = client.makefile('w')
    recv = client.makefile('r')
    send.write(json.dumps(join_msg) + '\r\n')
    send.flush()

    resp = recv.readline()
    updated = protocol.extract_json(resp)
    token = updated.token
    return token


def connect(host):
    '''
    Connects client to the server, returns a client connection
    '''
    try:
        server_address = (host, PORT)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print('connect successful')
        return client_socket
    except Exception as e:
        print('error connecting to server')
        #print(e)
        return False
