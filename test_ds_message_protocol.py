import ds_client as client
import ds_protocol as protocol


HOST = '168.235.86.101'

if __name__ == '__main__':
    cli = client.connect('168.235.86.101')
    token = client.join_as_user(cli, 'may', 'pwd')
    protocol.send_msg(cli, token, 'ohhimark', 'Hey!!')
