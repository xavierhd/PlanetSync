
from abc import ABCMeta, abstractmethod
import re

class DeviceType:
    LABEL = 1
    SSHFS = 2
    SAMBA = 3
    NFS = 4
    PHYSICAL = 5

def get_device_type(line):
    device_type = None
    lower_line = line.lower()
    if lower_line.startswith('sshfs#'):
        device_type = DeviceType.SSHFS
    elif lower_line.startswith('label='):
        device_type = DeviceType.LABEL
    elif lower_line.startswith('samba:'):
        device_type = DeviceType.SAMBA
    elif lower_line.startswith('nfs:'):
        device_type = DeviceType.NFS
    elif lower_line.startswith('/'):
        device_type = DeviceType.PHYSICAL
    else:
        raise Exception("Device is unknown for : " + line)
    return device_type

class FstabEntry(metaclass=ABCMeta):
    '''
    [Device] [Mount Point] [File System Type] [Options] [Dump] [Pass]
    '''
    original_line = None
    is_parsed_successfully = False

    # ?P<name> is an ID that can be retrieved with the match object
    # https://regex101.com/r/eJcqeD/7
    base_fields_regex = r"(?P<device>[\w\d_\+-.:@#=\/]+) *(?P<local_mount_path>(?:\/|[\w\d_\+-.]|(?:\\[^\w\d_\+-.]))+) *(?P<file_system_type>[\w\d_\+-.]+) *(?P<options>[\w\d_\+-.]+) *(?P<dump>[\d]) *(?P<pass>[\d])"
    base_fields = {
        'device': None,
        'local_mount_path': None,
        'file_system_type': None,
        'options': None,
        'dump': None,
        'pass': None
    }

    def __init__(self, line):
        self.parse_string_into_dict(line, self.base_fields, self.base_fields_regex)

    def parse_string_into_dict(self, string_to_parse, output_dictionary, regex):
        pattern = re.compile(regex)
        match = pattern.match(string_to_parse)
        if match:
            # groupindex is a dictionary-like of all the ?P<name> in the regex
            for group_name in pattern.groupindex:
                output_dictionary[group_name] = match.group(group_name)
            self.is_parsed_successfully = True
        else:
            print('FstabOperation::parse_line: The regex cannot match the string.\nregex:"{}"\nstring:"{}"'.format(regex, string_to_parse))

    @abstractmethod
    def rebuild(self):
        pass

# Label : LABEL=label
# Network ID

#     Samba : //server/share
#     NFS : server:/share
#     SSHFS : sshfs#user@server:/share 
class LabelFstabEntry(FstabEntry):
    '''
    Label : LABEL=label
    '''

    device_fields = {
        'device_path': None
    }

    def __init__(self, line):
        super().__init__(line)
        self.device_fields['device_path'] = self.base_fields['device']
        
class SambaFstabEntry(FstabEntry):
    '''
    Samba : //server/share
    '''

    device_fields = {
        'server': None,
        'file'
    }

    def __init__(self, line):
        super().__init__(line)
        self.device_fields['device_path'] = self.base_fields['device']

class NfsFstabEntry(FstabEntry):
    '''
    NFS : server:/share
    '''

    device_fields = {
        'device_path': None
    }

    def __init__(self, line):
        super().__init__(line)
        self.device_fields['device_path'] = self.base_fields['device']

class SshFsFstabEntry(FstabEntry):
    '''
    SSHFS : sshfs#user@server:/share 
    '''

    device_fields = {
        'device_path': None
    }

    def __init__(self, line):
        super().__init__(line)
        self.device_fields['device_path'] = self.base_fields['device']

class PhysicalDeviceFstabEntry(FstabEntry):
    '''
    Device : /dev/sdxy (not recommended)
    '''

    device_fields = {
        'device_path': None
    }

    def __init__(self, line):
        super().__init__(line)
        self.device_fields['device_path'] = self.base_fields['device']

