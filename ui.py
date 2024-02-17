# ui.py

# Leo Chao
# ychao13@uci.edu
# 76846188

from pathlib import Path

VALID_INPUT = ['L', 'Q', 'C', 'D', 'R', 'O', 'E', 'P', 'U']

'''
prints all avaliable commands
'''
def print_commands():
    print('\nHere\'s a list of commands that you can use!:\n')
    print('"L" - Lists contents in specified path')
    print('"Q" - Quit the program (You can also use Q during a command to leave that command)')
    print('"C" - Create a DSU file at given path')
    print('"D" - Deletes specified DSU file')
    print('"R" - Reads all data in specified DSU file')
    print('"O" - Loads content of specified DSU file')
    print('"E" - Edits content in DSU file loaded by C or O command')
    print('"P" - Prints specified content stored in DSU filed loaded by C or O command')
    print('"U" - Post selected journal entry onto the DSP server')
    
'''
reads input from user in a user friendly manner
'''
def read_input():
    inp = input().split()
    while not inp[0].upper() in VALID_INPUT or len(inp[0]) > 1:
        print('Invalid input, please try again\nHere are the valid inputs:')
        print_commands()
        inp = input().split()
    lst = edit_input(inp)
    
    if lst[0] == 'L': lst = list_content(lst)
    elif lst[0] == 'Q': return lst[0]
    elif lst[0] == 'C': lst = create_file(lst)
    elif lst[0] == 'D': lst = delete_file(lst)
    elif lst[0] == 'R': lst = read_file(lst)
    elif lst[0] == 'O': lst = load_file(lst)
    elif lst[0] == 'E': lst = edit_file(lst)
    elif lst[0] == 'P': lst = print_file(lst)
    elif lst[0] == 'U': return lst[0] 

    return lst

'''
turns input into a list, also makes sure if path includes whitespaces they aren't excluded
'''
def edit_input(lst, space = ''):
    fnl = []
    name = ""
    inp = False
    for i in lst:
        if i[0] == '"' or i[0] == '\'': inp = True
        if i[-1] == '"' or i[-1] == '\'': inp = False
        name += i + ' '
        if inp == False:
            fnl.append(name.replace('"', '').replace('\'', '').strip())
            name = ""
    return(fnl)

def get_path(lst, action):
    while len(lst) == 1:
        path = input(f'Please enter the {action} using the following format: "PATH".\n')
        if path.upper() == 'Q': return None
        itempath = Path(path.replace('"', '').replace('\'', ''))
        if itempath.exists():
            lst.append(path)
        else:
            print('Invalid path or path missing, try again')
    return lst

def get_commands(lst, spc = False):
    commands = input()
    for i in commands.split():
        lst.append(i)
    spacing = ''
    if spc: spacing = ' '
    return edit_input(lst, spacing)

def get_user_info(name, path):
    print(f'Your file called {name} will soon be created at {path}!\nPlease enter the following information.\n')
    ip = input('IP Address: (required): ')
    username = input('Username (required): ')
    password = input('Password (required): ')
    bio = input('Biography: (optional)')

    return ip, username, password, bio

def list_content(lst):
    lst = get_path(lst, 'path that you want load')
    if lst == None: return None
    print('Here are the avaliable commands:\nIf using multiple commands, enter them all in one line seperated with whitespaces:\nPress enter to skip this step.\n')
    print('-r - Recursively prints contents in all subfolders')
    print('-f - Prints files only')
    print('-s - Only outputs files that match given file name. Use format: -s "PATH"')
    print('-e - Only outputs files that match given file extension. Use format: -e "EXTENSION"')
    return get_commands(lst, False)

    
def create_file(lst):
    lst = get_path(lst, 'path to where you want your file to be created')
    if lst == None: return None
    name = input('Please enter what you\'d like to name the file in the following format: -n "NAME"\n')
    for i in name.split():
        lst.append(i)
    return edit_input(lst)
    
def delete_file(lst):
    lst = get_path(lst, 'path to the file you want to delete')
    if lst == None: return None
    return edit_input(lst)

def read_file(lst):
    lst = get_path(lst, 'path to the file you want to read')
    if lst == None: return None                   
    return edit_input(lst)

def load_file(lst):
    lst = get_path(lst, 'path to the file you want to load')
    if lst == None: return None
    return edit_input(lst)

def edit_file(lst):
    print('Here are the avaliable commands:\nIf using multiple commands, enter them all in one line seperated with whitespaces:\nPress enter to skip this step.\n')
    print('-usr - Update username. Use format: -usr "USERNAME"')
    print('-pwd - Update password. Use format: -pwd "PASSWORD"')
    print('-bio - Update biography. Use format: -bio "BIOGRAPHY"')
    print('-addpost - Add a new post. Use format: -addpost "NEW POST"')
    print('-delpost - Delete an existing post. Use format: -delpost "POST ID"')

    return get_commands(lst, True)
    
def print_file(lst):
    print('Here are the avaliable commands:\nIf using multiple commands, enter them all in one line seperated with whitespaces:\nPress enter to skip this step.\n')
    print('-usr - Print username.')
    print('-pwd - Print password.')
    print('-bio - Print biography.')
    print('-posts - Print all existing posts and their ID.')
    print('-post - Print a specific post. Use format: -post "POST ID"')
    print('-all - Print everything stored in profile.')

    return get_commands(lst, True)

