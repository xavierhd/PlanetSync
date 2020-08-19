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
from fstab.fstab_entry import FstabEntry, LabelFstabEntry, UuidFstabEntry, SambaFstabEntry, NfsFstabEntry, SshFsFstabEntry, PhysicalDeviceFstabEntry
from i18n import language_selector
from utils.stacktrace_helper import full_stack

fstab = FstabFile('../test/test_fstab_file/happy_full')
i18n_text = language_selector.get_lang('english')

answer_name = 'choice'
choice_back = i18n_text['general']['back']
choice_exit = i18n_text['general']['exit']
choice_delete = '[{}]'.format(i18n_text['general']['delete'])

prefix_edit = '[{}] '.format(i18n_text['general']['edit'])
indentation_prefix_edit = ' ' * (4 + len(prefix_edit))

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
        return lambda: display_mount_base_field(answer[answer_name])

def display_mount_base_field(mount_name):
    text_base_fields = i18n_text['mount']['base_fields']
    message = i18n_text['mount']['message']
    
    edit_choices = []
    entry = fstab.entries[mount_name]
    for attribute in entry.base_fields:
        name = text_base_fields[attribute]['name']
        data_value = entry.base_fields[attribute]
        description = text_base_fields[attribute]['description']
        edit_choices.append({
            'name': '{edit} {name:18.18}  ({description})\n{spaces}Value: {data_value}\n'.format(
                edit=prefix_edit,
                name=name,
                data_value=data_value,
                description=description,
                spaces=indentation_prefix_edit),
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
        confirm_question = i18n_text['mount']['delete_confirm']['question'].format(mount_name)
        yes = i18n_text['mount']['delete_confirm']['yes']
        no = i18n_text['mount']['delete_confirm']['no']
        is_delete_confirmed = confirm_choice(confirm_question, yes, no)
        if is_delete_confirmed:
            fstab.remove(mount_name)
            fstab.commit()
            return MOVE_BACK_ONE_LEVEL
    elif answer[answer_name] in entry.base_fields:
        attribute = answer[answer_name]
        if attribute == 'device':
            return lambda: display_device(entry)
        elif attribute == 'local_mount_path':
            pass
        elif attribute == 'file_system_type':
            pass
        elif attribute == 'options':
            pass
        elif attribute == 'dump':
            pass
        elif attribute == 'pass_number':
            pass
        return lambda: display_attribute_fields(answer[answer_name])

def display_device(entry: FstabEntry):
    device_type = entry.get_device_type()
    device_type_text = i18n_text['mount']['base_fields']['device']['types'][device_type]
    device_fields_text = device_type_text['device_fields']
    message = '{name:7}: {description}'.format(
        name=device_type_text['name'],
        description=device_type_text['description'])
    edit_choices = []
    for attribute in entry.device_fields:
        name = device_fields_text[attribute]['name']
        data_value = entry.device_fields[attribute]
        description = device_fields_text[attribute]['description']
        edit_choices.append({
            'name': '{edit} {name:18.18}  ({description})\n{spaces}Value: {data_value}\n'.format(
                edit=prefix_edit,
                name=name,
                data_value=data_value,
                description=description,
                spaces=indentation_prefix_edit),
            'value': attribute
        })
    choices = edit_choices + [Separator(), choice_back]
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
    elif answer[answer_name] in entry.device_fields:
        display_edit_text_attribute()

def display_edit_text_attribute():
    pass

if __name__ == '__main__':
    main()
