
from abc import ABCMeta, abstractmethod
import re

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
    
    # ?P<name> is an ID that can be retrieved with the match object
    # Test this regex with : https://regex101.com/r/eJcqeD/9
    base_fields_regex = r"(?P<device>.+?) +(?P<local_mount_path>.+?) +(?P<file_system_type>.+?) +(?P<options>.+?) +(?P<dump>.+?) +(?P<pass_number>.+?)"
    
    base_fields = {
        'device': None,
        'local_mount_path': None,
        'file_system_type': None,
        'options': None,
        'dump': None,
        'pass_number': None,
    }

    device_fields = {}

    def __init__(self, line):
        self.original_line = line
        self.base_fields = self.parse_string_into_dict(line, self.base_fields_regex)
        self.device_fields = self.parse_string_into_dict(self.base_fields['device'], self.get_device_regex())

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
            raise Exception('The regex cannot match the string.\nregex:"{}"\nstring:"{}"'.format(regex, string_to_parse))
        return result

    def to_line(self):
        device_template = self.get_device_template()
        self.base_fields['device'] = device_template.format(**self.device_fields)
        return "{device} {local_mount_path} {file_system_type} {options} {dump} {pass_number}".format(**self.base_fields)

    @abstractmethod
    def get_device_regex(self):
        pass

    @abstractmethod
    def get_device_template(self):
        pass

    @abstractmethod
    def get_device_type(self):
        pass

class LabelFstabEntry(FstabEntry):
    '''
    Label : LABEL=label
    '''
    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return "LABEL={label}"

    def get_device_regex(self):
        # Test this regex with: https://regex101.com/r/efMcmb/1
        return r"(?i)LABEL=(?P<label>.+)"
    
    def get_device_type(self):
        return 'label'

class UuidFstabEntry(FstabEntry):
    '''
    UUID : UUID=label
    '''
    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return "UUID={uuid}"

    def get_device_regex(self):
        # Test this regex with: https://regex101.com/r/efMcmb/1
        return r"(?i)UUID=(?P<uuid>.+)"
    
    def get_device_type(self):
        return 'uuid'
        
class SambaFstabEntry(FstabEntry):
    '''
    Samba : //server/share
    '''
    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return "//{server}/{share}"

    def get_device_regex(self):
        return r"\/\/(?P<server>.+?)\/(?P<share>.+)"
    
    def get_device_type(self):
        return 'samba'

class NfsFstabEntry(FstabEntry):
    '''
    NFS : server:/share
    '''
    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return "{server}/{share}"

    def get_device_regex(self):
        # Test this regex with: https://regex101.com/r/933ygI/1
        return r"(?P<server>.+?)\/(?P<share>.+)"
    
    def get_device_type(self):
        return 'nfs'

class SshFsFstabEntry(FstabEntry):
    '''
    SSHFS : sshfs#user@server:/share
    fuse delay_connect,comment=sshfs,noauto,users,exec,uid=1000,gid=1000,allow_other,reconnect,transform_symlinks,BatchMode=yes,port=22,IdentityFile=/local/path/to/privatekey.pem
    '''

    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return "sshfs#{user}@{server}:{share}"

    def get_device_regex(self):
        # Test this regex with: https://regex101.com/r/eBo9mF/3
        return r"(?i)sshfs#(?P<user>.+?)@(?P<server>.+?):(?P<share>.+)"
    
    def get_device_type(self):
        return 'sshfs'

class PhysicalDeviceFstabEntry(FstabEntry):
    '''
    Device : /dev/sdxy (not recommended)
    '''
    def __init__(self, line):
        super().__init__(line)

    def get_device_template(self):
        return '{}'

    def get_device_regex(self):
        return r'.*'
    
    def get_device_type(self):
        return 'device'
