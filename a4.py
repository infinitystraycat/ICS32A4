# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Maya Fukunaga
# mfukuna1@uci.edu
# 66943792
import shlex

from pathlib import Path
from Profile import Profile, Post
import ui
import a5gui as gui

EXTENSION = '.dsu'
NEWP = '-n'
thepath = ''


def create_file(tokens):
    '''
    Call to create a new file of .dsu type when called.
    Will load the file if the file type already exists.
    '''
    path = Path(tokens[1])
    try:
        if tokens[2] == NEWP:
            file_name = tokens[3] + EXTENSION
            newpath = path/Path(file_name)
            if not newpath.exists():
                file = open(newpath, 'w', encoding="utf-8")
                print(newpath)
                file.close()
                prof = ui.profileCreate()
                Profile.save_profile(prof, newpath)
                bio = ''.join(prof.bio)
                usr = ''.join(prof.username)
                pwd = ''.join(prof.password)
                print(f'Created Profile: Name {usr}, '
                      f'Password {pwd}, Bio {bio}')
            else:
                print('File already exists. Loading your file...')
                prof = Profile()
                prof.load_profile(newpath) 
                newpath.touch()
                print(newpath)
            return prof, str(newpath)
        else:
            print('ERROR: Proper command not given')
            return None, None
    except:
        print('Error: proper commands/path not given')
        return None, None


def add_bio(prof, bio):
    '''
    Use to add or change the bio of the open, current profile.
    '''
    prof.bio = bio
    bio = ''.join(prof.bio)
    usr = ''.join(prof.username)
    pwd = ''.join(prof.password)
    print(f'Updated Profile: Name {usr}, '
          f'Password {pwd}, Bio {bio}')
    return prof


def add_user_name(prof, uname):
    '''
    Use to add or change the name of the open, current profile.
    '''
    prof.username = uname
    bio = ''.join(prof.bio)
    usr = ''.join(prof.username)
    pwd = ''.join(prof.password)
    print(f'Updated Profile: Name {usr}, '
          f'Password {pwd}, Bio {bio}')
    return prof


def add_password(prof, upass):
    '''
    Use to add or change the password of the open, current profile.
    '''
    prof.password = upass
    bio = ''.join(prof.bio)
    usr = ''.join(prof.username)
    pwd = ''.join(prof.password)
    print(f'Updated Profile: Name {usr}, '
          f'Password {pwd}, Bio {bio}')
    return prof


def add_post(prof, post):
    '''
    Use this to add a post to the current profile.
    Should return the contents of the post
    that was added
    '''
    newpost = Post(post)
    prof.add_post(newpost)
    past = prof.get_posts()
    print('Added post: ')
    print(''.join(past[-1].entry))
    return prof


def delete_post(prof, index):
    '''
    Use this to delete a post of the given index
    '''
    index = index - 1
    prof.del_post(index)
    print('Finished deleting post')
    return prof


def open_file(path):
    '''
    Loads a file of a given path.
    Will give an error if the path is not a proper dsu file.
    '''
    prof = Profile()
    path = Path(path)
    if path.suffix == (EXTENSION):
        path.touch()
        prof.load_profile(path)
        print(f'Loaded file: {path}')
        return prof, path
    else:
        print('ERROR: Can not open the file, needs to be a dsu file.')
        return False
        


def profile_editor(savePath, prof, tokens):
    '''
    Use to take and operate based on commands to alter a profile.
    '''
    newProf = Profile()
    new_opt = find_opt(tokens)
    if len(new_opt) > 0:
        for option, item in new_opt.items():
            if option == '-usr':
                newProf = add_user_name(prof, item)
            elif option == '-pwd':
                newProf = add_password(prof, item)
            elif option == '-bio':
                newProf = add_bio(prof, item)
            elif option == '-addpost':
                newProf = add_post(prof, item)
            elif option == '-delpost':
                newProf = delete_post(prof, int(item[0]))
            newProf.save_profile(savePath)
    else:
        print('Error: No valid options')


def printer(prof,tokens):
    '''
    Use to print information in the given profile.
    Users can specify what kind of information that they want printed.
    '''
    tokens = tokens[1:]
    new_opt = find_opt(tokens)
    if len(new_opt.items()) > 0:
        for option, item in new_opt.items():
            if option == '-usr':
                print(''.join(prof.username))
            elif option == '-pwd':
                print(''.join(prof.password))
            elif option == '-bio':
                print(''.join(prof.bio))
            elif option == '-posts':
                posts = prof.get_posts()
                i = 0
                while i < len(posts):
                    print(''.join(posts[i].entry))
                    i += 1
            elif option == '-post':
                id_orig = int(''.join(item))
                id_num = id_orig-1
                posts = prof.get_posts()
                if len(posts) == 0:
                    print('No posts')
                else:
                    print(f'Here is the post of post id {id_orig}: ')
                    print(''.join(posts[id_num].entry))
            elif option == '-all':
                print_all(prof)
    else:
        print('Error: no options given after command')


def print_all(prof):
    '''
    Use to print all of the information stored in a profile.
    '''
    name = ''.join(prof.username)
    password = ''.join(prof.password)
    bio = ''.join(prof.bio)
    print(f'Username: {name}')
    print(f'Password: {password}')
    print(f'Bio: {bio}')
    print('Posts: ')
    posts = prof.get_posts()
    i = 0
    while i < len(posts):
        print(''.join(posts[i].entry))
        i += 1


def admin_mode():
    '''
    Called when the user wants to use admin mode.
    This will not give any specific instructions and is not userfriendly
    Allows for multiple inputs at the same time.
    '''
    savepath = Path()
    prof = None
    while True:
        try:
            userIn = input()
            tokens = shlex.split(userIn)
            command = tokens[0].lower()
            if command == 'q':
                print('Exiting program...')
                break

            
            if command == 'c':
                prof, savepath = create_file(tokens)
            elif command == 'o':
                path = tokens[1]
                prof, savepath = open_file(path)
            elif command == 'e':
                profile_editor(savepath, prof, tokens)
            elif command == 'p':
                printer(prof,tokens)
            else:
                print('Error')
        except:
            print('Error: please input a valid command')


def find_opt(tokens):
    '''
    Splits the parts of the user input to see which are options of a command,
    and what the values are of each.
    Not intended to take the same commands at the same times (can't do post1,
    post 2 on the same line)
    '''
    options = {}
    current_option = None
    for token in tokens:
        if token.startswith('-'):
            current_option = token
            options[current_option] = []
        elif current_option:
            options[current_option].append(token)
            options[current_option].append(" ")
    return options



def run():
    '''
    main running code
    '''
    ui.userInteraction()


if __name__ == '__main__':
    gui.main()
    #run()