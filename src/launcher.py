#!/usr/bin/env python3
"""
PlanetSync
The SSH Directory Mounter
Create an ssh file share with your home's dynamic IP server
"""
import sys
import uuid
from PyInquirer import prompt, Separator
from pyfiglet import figlet_format
from pprint import pprint

from fstab import FstabFile
from i18n import language_selector

fstab = FstabFile('../test/test_fstab_file/happy_full')
i18n_text = language_selector.get_lang('english')

answer_name = 'choice'
choice_back = i18n_text['general']['back']
choice_exit = i18n_text['general']['exit']

MOVE_BACK_ONE_LEVEL = uuid.uuid4()

def main():
    try:
        loop(display_main_menu)
    except KeyboardInterrupt:
        print('Exiting.')
    print("Thank you, please come again!")

def loop(lambda_to_loop):
    list_to_loop = [lambda_to_loop]
    while list_to_loop:
        remove_from_list = True
        try:
            value = list_to_loop[-1]()
        except KeyboardInterrupt:
            print('Moving back one level.')
        except:
            print('Unexpected error raised: ', full_stack())
        else:
            remove_from_list = False

        if remove_from_list or value == MOVE_BACK_ONE_LEVEL:
            list_to_loop.pop()
        elif callable(value):
            list_to_loop.append(value)

def full_stack():
    '''
    Shameless copypasta : https://stackoverflow.com/a/16589622
    Get a complete exception stack trace.
    '''
    import traceback
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
         stackstr += '  ' + traceback.format_exc()[len(trc):]
    return stackstr

def confirm_choice(confirm_text, yes_text, no_text):
    choice_yes = 'y'
    choice_no = 'n'
    choices = [
        {
            'name': no_text,
            'value': choice_no
        },
        {
            'name': yes_text,
            'value': choice_yes
        }
    ]
    questions = [
        {
            'type': 'list',
            'name': answer_name,
            'message': confirm_text,
            'choices': choices
        }
    ]
    answer = prompt(questions)
    return (answer and answer[answer_name] == choice_yes)

def display_main_menu():
    print(figlet_format(i18n_text['menu']['title'], font="slant"))
    print(i18n_text['menu']['info'])
    message = i18n_text['menu']['message']
    choices = i18n_text['menu']['choices'] + [Separator(), choice_exit]
    questions = [
        {
            'type': 'list',
            'name': answer_name,
            'message': message,
            'choices': choices
        }
    ]
    answer = prompt(questions)
    if not answer or answer[answer_name] == choice_exit:
        return MOVE_BACK_ONE_LEVEL
    else:
        index = choices.index(answer[answer_name])
        actions = [
            display_quick_mount,
            display_add_sshKey,
            display_mount_fstab,
            display_umount_fstab,
            display_all_mount
        ]
        return actions[index]

def display_quick_mount():
    return MOVE_BACK_ONE_LEVEL

def display_add_sshKey():
    return MOVE_BACK_ONE_LEVEL

def display_mount_fstab():
    return MOVE_BACK_ONE_LEVEL

def display_umount_fstab():
    return MOVE_BACK_ONE_LEVEL

def display_all_mount():
    message = i18n_text['all_mount']['message']
    fstab_server = fstab.get_server_list()
    choices = fstab_server + [Separator(), choice_back]
    questions = [
        {
            'type': 'list',
            'name': answer_name,
            'message': message,
            'choices': choices
        }
    ]
    answer = prompt(questions)
    if not answer or answer[answer_name] == choice_back:
        return MOVE_BACK_ONE_LEVEL
    else:
        return lambda: display_single_mount(answer[answer_name])

def display_single_mount(mount_name):
    prefixes = i18n_text['single_mount']['attributes']
    message = i18n_text['single_mount']['message'].format(mount_name)
    edit = i18n_text['general']['edit']
    choice_delete = i18n_text['general']['delete'] + ' ' + mount_name
    
    edit_choices = []
    data = fstab.data[mount_name]
    for attribute in data:
        prefix = prefixes[attribute]
        data_value = data[attribute]
        edit_choices.append({
            'name': '[' + edit + ']' + prefix + ': ' + data_value,
            'value': attribute
        })
    choices = edit_choices + [Separator(), choice_delete, Separator(), choice_back]
    questions = [
        {
            'type': 'list',
            'name': answer_name,
            'message': message,
            'choices': choices
        }
    ]
    answer = prompt(questions)
    if not answer or answer[answer_name] == choice_back:
        return MOVE_BACK_ONE_LEVEL
    elif answer[answer_name] == choice_delete:
        confirm_question = i18n_text['single_mount']['delete_confirm']['question'].format(mount_name)
        yes = i18n_text['single_mount']['delete_confirm']['yes']
        no = i18n_text['single_mount']['delete_confirm']['no']
        is_delete_confirmed = confirm_choice(confirm_question, yes, no)
        if is_delete_confirmed:
            fstab.remove(mount_name)
            return MOVE_BACK_ONE_LEVEL

if __name__ == '__main__':
    main()
