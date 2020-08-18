
from abc import ABCMeta, abstractmethod
import re

class DeviceType:
    LABEL = 1
    SSHFS = 2
    SAMBA = 3
    NFS = 4
    PHYSICAL = 5

def build_fstab_entry(line):
    entry = None
    lower_line = line.lower()
    if lower_line.startswith('sshfs#'):
        entry = SshFsFstabEntry(line)
    elif lower_line.startswith('label='):
        entry = LabelFstabEntry(line)
    elif lower_line.startswith('uuid='):
        entry = UuidFstabEntry(line)
    elif lower_line.startswith('//'):
        entry = SambaFstabEntry(line)
    elif lower_line.startswith('/'):
        entry = PhysicalDeviceFstabEntry(line)
    else:
        entry = NfsFstabEntry(line)
    return entry

class FstabEntry(metaclass=ABCMeta):
    '''
    [Device] [Mount Point] [File System Type] [Options] [Dump] [Pass]
    '''
    original_line = None
    device_name = None
    
    # ?P<name> is an ID that can be retrieved with the match object
    # Test this regex with : https://regex101.com/r/eJcqeD/7
    base_fields_regex = r"(?P<device>[\w\d_\+-.:@#=\/]+) *(?P<local_mount_path>(?:\/|[\w\d_\+-.]|(?:\\[^\w\d_\+-.]))+) *(?P<file_system_type>[\w\d_\+-.]+) *(?P<options>[\w\d_\+-.]+) *(?P<dump>[\d]) *(?P<pass_number>[\d])"
    
    base_fields = {
        'device': None,
        'local_mount_path': None,
        'file_system_type': None,
        'options': None,
        'dump': None,
        'pass_number': None,
    }

    device_fields = {}

    def __init__(self, line, device_name, device_regex):
        self.original_line = line
        self.device_name = device_name
        self.base_fields = self.parse_string_into_dict(line, self.base_fields_regex)
        if device_regex:
            self.device_fields = self.parse_string_into_dict(self.base_fields['device'], device_regex)

    def parse_string_into_dict(self, string_to_parse, regex):
        '''
        The regex group (?P\\<name\\>) will be the returned dictionnary's keys.
        Raise if the string cannot be matched by the regex.
        '''
        result = {}
        pattern = re.compile(regex)
        match = pattern.match(string_to_parse)
        if match:
            for group_name in pattern.groupindex:  # Note, pattern.groupindex is a dictionary-like of all the ?P<name> in the regex.
                result[group_name] = match.group(group_name)
        else:
            raise 'The regex cannot match the string.\nregex:"{}"\nstring:"{}"'.format(regex, string_to_parse)
        return result

    def to_line(self):
        if self.device_fields:
            device_template = self.get_device_template()
            self.base_fields['device'] = device_template.format(**self.device_fields)
        "{device} {local_mount_path} {file_system_type} {options} {dump} {pass}".format(self.base_fields)

    @abstractmethod
    def get_device_template(self):
        pass

class LabelFstabEntry(FstabEntry):
    '''
    Label : LABEL=label
    '''
    # Test this regex with: https://regex101.com/r/efMcmb/1
    regex = r"(?i)LABEL=(?P<label>.+)"

    def __init__(self, line):
        super().__init__(line, 'label', self.regex)

    def get_device_template(self):
        return "LABEL={label}"

class UuidFstabEntry(FstabEntry):
    '''
    Label : LABEL=label
    '''
    # Test this regex with: https://regex101.com/r/efMcmb/1
    regex = r"(?i)UUID=(?P<uuid>.+)"

    def __init__(self, line):
        super().__init__(line, 'label', self.regex)

    def get_device_template(self):
        return "UUID={label}"
        
class SambaFstabEntry(FstabEntry):
    '''
    Samba : //server/share
    '''
    # Test this regex with: https://regex101.com/r/efMcmb/1
    regex = r"\/\/(?P<server>.+?)\/(?P<share>.+)"

    def __init__(self, line):
        super().__init__(line, 'samba', self.regex)

    def get_device_template(self):
        return "//{server}/{share}"

class NfsFstabEntry(FstabEntry):
    '''
    NFS : server:/share
    '''
    # Test this regex with: https://regex101.com/r/933ygI/1
    regex = r"(?P<server>.+?)\/(?P<share>.+)"

    def __init__(self, line):
        super().__init__(line, 'nfs', self.regex)

    def get_device_template(self):
        return "{server}/{share}"

class SshFsFstabEntry(FstabEntry):
    '''
    SSHFS : sshfs#user@server:/share
    fuse delay_connect,comment=sshfs,noauto,users,exec,uid=1000,gid=1000,allow_other,reconnect,transform_symlinks,BatchMode=yes,port=22,IdentityFile=/local/path/to/privatekey.pem
    '''
    # Test this regex with: https://regex101.com/r/eBo9mF/3
    regex = r"(?i)sshfs#(?P<user>.+?)@(?P<server>.+?):(?P<share>.+)"

    def __init__(self, line):
        super().__init__(line, 'sshfs', self.regex)

    def get_device_template(self):
        return "sshfs#{user}@{server}:{share}"

class PhysicalDeviceFstabEntry(FstabEntry):
    '''
    Device : /dev/sdxy (not recommended)
    '''

    def __init__(self, line):
        super().__init__(line, 'device', None)

    def get_device_template(self):
        return '{}'
