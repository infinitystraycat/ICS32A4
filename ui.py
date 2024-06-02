# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792

from Profile import Profile
from pathlib import Path
import a4
import ds_client as client

SERVERN = '168.235.86.101'
PORT = 3021


def profileCreate():
    uName = input('Please enter the user name: ')
    uPass = input('Please enter the password: ')
    bio = input('Please enter the bio: ')
    prof = Profile(SERVERN, uName, uPass)
    prof.bio = bio
    return prof


def userInteraction():
    done1 = False
    done2 = False
    print('Welcome!')
    savePath = Path()
    newprof = None
    sName = ''
    while not done1:
        try:
            command = input('Do you want to create or '
                            'load a DSU file (type \'c\' to '
                            'create or \'o\' to load): \n').lower().strip()
            if command == 'q':
                done1 = True
                done2 = True
            if command == 'admin':
                a4.admin_mode()
                done1 = True
                done2 = True
                break
            elif command == 'o':
                path = input('Great! What is file path name that you '
                             'want to access?\n').replace('"', '')
                path = path.replace("'", '').strip()
                path = Path(path)
                finished, path = a4.open_file(path)
                if not finished:
                    done1 = False
                else:
                    done1 = True
                    newprof = finished
                    savePath = path
            elif command == 'c':
                path = input('Great! Where would you like to place your '
                             'file?\n').replace('"', '').strip()
                name = input('What would you like to name your new file?\n')
                prof, path = a4.create_file(['c', path, '-n', name])
                if prof:
                    done1 = True
                    savePath = path
                    newprof = prof
                    break
                else:
                    print('none for ')
                    done1 = False
        except Exception as e:
            print('Error: ' + str(e))
            print('Please enter a valid input')

    while not done2:
        try:
            command = input('What would you like to do with your file? '
                            '(Type \'e\' to edit, \'p\' to '
                            'print, and \'u\' to upload '
                            'online, \'q\' to quit.)\n').lower().strip()
            if command == 'q':
                break
            elif command == 'e':
                editProfile(newprof, savePath)
            elif command == 'p':
                printProfile(newprof)
            elif command == 'u':
                sName = uploadOnline(newprof, sName)
            else:
                print('Please enter a valid command')
        except Exception as e:
            print('Error: ' + str(e))
            print('Please enter a valid input')

    print('Thank your for using us!')


def uploadOnline(newprof, sName):
    validity = False
    if len(sName) == 0:
        servername = input('Please enter the server name \n')
        servername = servername.strip(('\'"'))
    else:
        servername = sName

    uname = newprof.username
    passw = newprof.password
    bio = ''.join(newprof.bio)
    post = newprof.get_posts()
    i = 0
    topost = ''

    command = input('Please enter what you would like to do: \n'
                    'q if you want to quit this option \n'
                    'p if you want to upload a post\n'
                    'b if you want to update your bio \n'
                    )
    command = command.strip().lower()

    if command == 'b':
        topost = 'nopost'
        validity = client.send(servername, PORT, uname, passw,
                               str(topost), str(bio))
    elif command == 'p':
        if len(post) == 0:
            validity = client.send(servername, PORT, uname, passw,
                                   str(topost), str(bio))
        else:
            i = 0
            print("Current Posts:")
            while i < len(post):
                print(str(i+1) + ': ' + ''.join(post[i].entry))
                i += 1
            numPosts = input("Which post would you like to post?\n")
            i = 0
            while i < len(post):
                if i+1 == int(numPosts):
                    topost = ''.join(post[i].entry)
                    validity = client.send(servername, PORT, uname, passw,
                                           str(topost), str(bio))
                    if validity:
                        print('Profile was successfully updated online.')
                    else:
                        print('Profile could not be uploaded properly. '
                              'Please check your inputs.')
                i += 1
    return servername


def printProfile(newprof):
    print('Please enter what you would like to print:')
    print('usr to print username')
    print('pwd to print password')
    print('bio to print bio')
    print('posts to print all posts')
    print('post to print a specific post')
    print('all to print everything stored in your profile')
    option = input().lower().strip()
    if option == 'usr':
        a4.printer(newprof, ['p', '-usr', ''])
    elif option == 'pwd':
        a4.printer(newprof, ['p', '-pwd', ''])
    elif option == 'bio':
        a4.printer(newprof, ['p', '-bio', ''])
    elif option == 'posts':
        a4.printer(newprof, ['p', '-posts', ''])
    elif option == 'post':
        dpost = input('What is the number of the post that '
                      'you want to see? \n')
        a4.printer(newprof, ['p', '-post', dpost])
    elif option == 'all':
        a4.printer(newprof, ['p', '-all', ''])
    else:
        print('Please enter a valid input')


def editProfile(newprof, savePath):
    print('Please enter what you would like to edit: '
          '(Remember to put all entries between quotation marks)')
    print('u to change username')
    print('p to change password')
    print('b to change bio')
    print('a to add a post')
    print('d to delete a post')
    option = input().lower().strip()
    if option == 'u':
        user = input('What would you like to change your '
                     'username to?\n')
        a4.profile_editor(savePath, newprof, ['-usr', user])
    if option == 'p':
        passw = input('What would you like to change '
                      'your password to? \n')
        a4.profile_editor(savePath, newprof, ['-pwd', passw])
    if option == 'b':
        bio = input('What would you like to change your '
                    'bio to? \n')
        a4.profile_editor(savePath, newprof, ['-bio', bio])
    if option == 'a':
        post = input('What would you like your post to say \n')
        a4.profile_editor(savePath, newprof, ['-addpost', post])
    if option == 'd':
        dpost = input('What is the post number that you want '
                      'to delete? \n')
        a4.profile_editor(savePath, newprof, ['-delpost', dpost])
