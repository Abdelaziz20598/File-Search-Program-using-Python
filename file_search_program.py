"""
	Name: File Search Program
	Author: Abdelaziz Abdelfatah
	Email:Abdelaziz20598@gmail.com
	Modified: 23-12-2022

    A very simplified version of the file search engine project built with PySimpleGUI
    except using a listbox. When an item is click on, the program will attempt to open with the
    default program.
"""
# first creating a search engine import os
# for using the os.walk() function for indexing the drive  it is a generator function means it yields on result at a time either by iterating over it or calling it with next(generator())


# creating the search engine
import os
import sys
import time
from datetime import datetime

# creating the search engine graphic
import PySimpleGUI as sg


def search(values, window):
    window['-INFO-'].update(value='Searching for matches...')
    """Perform a search based on term and type"""
    global results
    # reset the results list
    results.clear()
    window['-RESULTLEN-'].update("")
    window['-RESULTS-'].update(values=results)

    # search for term and save new results
    for root, _, files in os.walk(values['-PATH-']):
        for file in files:
            if values['-ENDSWITH-'] and file.lower().endswith(values['-TERM-'].lower()):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
                window['-RESULTLEN-'].update(
                    f"number of files : {len(results)}")
            if values['-STARTSWITH-'] and file.lower().startswith(values['-TERM-'].lower()):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
                window['-RESULTLEN-'].update(
                    f"number of files : {len(results)}")
                
            if values['-CONTAINS-'] and values['-TERM-'].lower() in file.lower():
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
                window['-RESULTLEN-'].update(
                    f"number of files : {len(results)}")
                
            if values['-CREATIONTIME-'] and values['-TERM-'] == datetime.strptime(time.ctime(os.path.getctime(f'{root}\\{file}')), '%a %b %d %H:%M:%S %Y').strftime("%d-%m-%Y"):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
                window['-RESULTLEN-'].update(
                    f"number of files : {len(results)}")
            if values['-MODIFIEDTIME-'] and values['-TERM-'] == datetime.strptime(time.ctime(os.path.getmtime(f'{root}\\{file}')), '%a %b %d %H:%M:%S %Y').strftime("%d-%m-%Y"):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
                window['-RESULTLEN-'].update(
                    f"number of files : {len(results)}")

    sg.PopupOK('Finished!')
    window['-INFO-'].update('Enter a search term and press `Search`')


def open_file(file_name):
    """Attempt to open the file with the default program"""
    # probably should add error handling here for when a default program cannot be found.
   
    os.system( '"'+file_name+'"')
  


# create the main file search window
results = []
sg.change_look_and_feel('Black')
layout = [
    [sg.Text('Search Term', size=(11, 1)), sg.Input('', size=(40, 1), key='-TERM-'),
     sg.Radio('Contains', group_id='search_type', size=(
         10, 1), default=True, key='-CONTAINS-'),
     sg.Radio('StartsWith', group_id='search_type',
              size=(10, 1), key='-STARTSWITH-'),
     sg.Radio('EndsWith', group_id='search_type',
              size=(10, 1), key='-ENDSWITH-'),
     sg.Radio('Creation Time', group_id='search_type',
              size=(10, 1), key='-CREATIONTIME-'),
     sg.Radio('Modified Time', group_id='search_type',
              size=(10, 1), key='-MODIFIEDTIME-')
     ],
    [sg.Text('Search Path', size=(11, 1)), sg.Input('/..', size=(40, 1), key='-PATH-'),
     sg.FolderBrowse(size=(10, 1), key='-BROWSE-'),
     sg.Button('Search', size=(10, 1), key='-SEARCH-')],
    [sg.Text('Enter a search term and press `Search`', key='-INFO-'),
     sg.Text('', key='-RESULTLEN-')],
    [sg.Listbox(values=results, size=(100, 28), enable_events=True, key='-RESULTS-')]]

window = sg.Window('File Search Engine by Omar Abdelaziz',
                   layout=layout, finalize=True, return_keyboard_events=True)
window['-RESULTS-'].expand(expand_x=True, expand_y=True)


# main event loop
while True:
    event, values = window.read()
    if event is None:
        break
    if event == '-SEARCH-':
        search(values, window)
    if event == '-RESULTS-':
        file_name = values['-RESULTS-']
        if file_name:
            open_file(file_name[0])
