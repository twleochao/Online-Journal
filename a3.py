# a3.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

DSPHOST = "168.235.86.101"
PORT = 3021

from ds_client import send 
from pathlib import Path
from ui import print_commands, read_input, get_user_info, edit_input
from Profile import Profile, Post

'''
prints the paths to terminal, makes sure to follow options
'''
def printresults(content):
    content = Path(content)
    if specificname != "":
        if content.name == specificname: print(content)
    elif specificsuffix != "":
        if content.suffix == specificsuffix: print(content)
    else: print(content)

'''
goes through contents in the given path, going through files first then directories
'''
def see_contents(path, rec = False, fileonly = False):
    try:
        itempath = Path(path)
        contents = sorted(itempath.iterdir())
        for i in contents:
            if i.is_file():
                printresults(i)
        for i in contents:
            if i.is_dir():
                if not fileonly: printresults(i)
                if rec: see_contents(i, rec, fileonly)
    except (FileNotFoundError, NotADirectoryError):
        print("Path not found or not a directory, try again")


'''
creates new file in specified directory
'''
def create_file(path, name):
    name += '.dsu'
    filepath = Path(path).joinpath(name)
    try:
        if filepath.exists() and filepath.suffix == '.dsu':
            return load_content(filepath)

        filepath.touch()
        lst = get_user_info(name, path)
        if not lst[0] or not lst[1] or not lst[2]:
            print('Missing ip or username or password, please try again')
            lst = get_user_info(name, path)
        pf = Profile(lst[0], lst[1], lst[2])
        try:
            pf.bio = lst[3]
        except IndexError:
            pass
        pf.save_profile(filepath)
    except FileNotFoundError:
        print("Path not found, try again")
    return filepath, pf


'''
delete specific file, only works with dsu files
'''
def delete_file(path):
    filepath = Path(path)
    if filepath.suffix != '.dsu':
        print('ERROR')
        return

    try:
        filepath.unlink()
        print(f'{filepath} DELETED')
    except FileNotFoundError:
        print('File not found, try again')


'''
print contents of a dsu file
'''
def read_content(path):
    filepath = Path(path)
    if filepath.suffix != '.dsu':
        print('ERROR')
        return

    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if content: print(content)
            else: print('EMPTY')
    except FileNotFoundError:
        print('File not found, try again')

def load_content(path):
    filepath = Path(path)
    if filepath.suffix != '.dsu':
        print('ERROR, not .dsu file')
        return
    pf = Profile()
    pf.load_profile(path)
    print(f'{filepath.name} created by {pf.username} has been successfully loaded!')
    return filepath, pf

def edit_content(pf, lst):
    i = 0
    while i < len(lst):
        if lst[i] == '-usr':
            pf[1].username = lst[i+1]
        elif lst[i] == '-pwd':
            pf[1].password = lst[i+1]
        elif lst[i] == '-bio':
            pf[1].bio = lst[i+1]
        elif lst[i] == '-addpost':
            pst = Post()
            pst.set_entry(lst[i+1])
            pf[1].add_post(pst)
        elif lst[i] == '-delpost':
            posts = pf[1].get_posts()
            print(f'{lst[i+1]}: {posts[int(lst[i+1]) - 1]["entry"]} (DELETED)')
            pf[1].del_post(int(lst[i+1]) - 1)
        else:
            print('Error: Unknown command, please try again')
            return
        i += 2
    pf[1].save_profile(pf[0])

def print_content(pf, lst):
    i = 0
    while i < len(lst):
        if lst[i] == '-usr':
            print(f'Username: {pf[1].username}')
        elif lst[i] == '-pwd':
            print(f'Password: {pf[1].password}')
        elif lst[i] == '-bio':
            print(f'Biography: {pf[1].bio}')
        elif lst[i] == '-posts':
            posts = pf[1].get_posts()
            print('Posts:')
            for post in posts:
                print(f'{posts.index(post) + 1}: {post["entry"]}')
            i -= 1
        elif lst[i] == '-post':
            posts = pf[1].get_posts()
            print(f'{lst[i+1]}: {posts[int(lst[i+1]) - 1]["entry"]}')
        elif lst[i] == '-all':
            print(f'Username: {pf[1].username}')
            print(f'Password: {pf[1].password}')
            print(f'Biography: {pf[1].bio}')
            posts = pf[1].get_posts()
            print('Posts:')
            for post in posts:
                print(f'{posts.index(post) + 1}: {post["entry"]}')
            i -= 1
        else:
            print('Error: Unknown command, please try again')
            return
        i += 2

def post_journal(pf, idx):
    posts = pf[1].get_posts()
    if not is_int(idx) or int(idx) < 0:
        print('Invalid index, try again')
        return

    idx = int(idx)
    if idx == 0: 
        res = send(pf[1].dsuserver, PORT, pf[1].username, pf[1].password, None, pf[1].bio)
        if res: print('Bio has been successfully updated!')
        else: print('An error has occured')
    else:
        res = send(pf[1].dsuserver, PORT, pf[1].username, pf[1].password, posts[idx - 1]["entry"], pf[1].bio)
        if res: print(f'Journal #{idx}: {posts[idx - 1]["entry"]} has been successfully posted!') 
        else: print('An error has occured with uploading, please try again')

def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def main():
    print('Welcome to your Personal Journal! Press enter to begin: ', end="")
    run()

def run(lst = [], admin = None, profile_info = None): 
    if admin == None: admin = input()

    global specificname
    global specificsuffix
    runagain = True
    rec = False
    fileonly = False

    if admin != 'admin':
        print_commands()
        lst = read_input()
    else:
        lst = edit_input(input().split())

    if lst != None:
        if '-r' in lst: rec = True
        if '-f' in lst: fileonly = True
        if '-s' in lst: specificname = lst[lst.index('-s') + 1]
        if '-e' in lst: 
            specificsuffix = lst[lst.index('-e') + 1] 
            if specificsuffix[0] != '.':
                specificsuffix = '.' + specificsuffix
        try:
            cmd = lst[0]
            if cmd == 'Q':
                runagain = False
            elif cmd == 'L':
                see_contents(lst[1], rec, fileonly)
            elif cmd == 'C':
                profile_info = create_file(lst[1], lst[3])
            elif cmd == 'D':
                delete_file(lst[1])
            elif cmd == 'R':
                read_content(lst[1])
            elif cmd == 'O':
                profile_info = load_content(lst[1])
            elif cmd == 'E' or cmd == 'P' or cmd == 'U':
                try: 
                    if cmd == 'E': edit_content(profile_info, lst[1:])
                    elif cmd == 'P': print_content(profile_info, lst[1:])
                    else: post_journal(profile_info, lst[1])
                except TypeError:
                    print('No profile loaded, try using the C or O commands first')
            else:
                print('Command not found, please try again')
        except IndexError:
            print('Error: Value out of bounds')

    if runagain: run(lst, admin, profile_info)

if __name__ == "__main__":
    main()
