
#The profile-specific information for a few select versions
PROFILES = { 'bcm4339_6.37.34.40' :
                {'ram_dump_offset'    : 0x180000,
                 'freelist_address'   : 0x180E68,
                 'main_chunk_address' : 0x1EBE78,
                 'max_heap_address'   : 0x23D6D0},
             'bcm4358_7.112.201.1' :
                {'ram_dump_offset'    : 0x180000,
                 'freelist_address'   : 0x1820CC,
                 'main_chunk_address' : 0x1E8C28,
                 'max_heap_address'   : 0x23deb4},
           }

#The currently selected profile
current_profile = None

def set_profile(profile_name):
    '''
    Sets the currently selected profile.
    '''
    global current_profile
    current_profile = profile_name

def get_profile_def(def_name):
    '''
    Retrieves the given profile definition from the selected profile
    '''
    if current_profile == None:
        raise Exception("Profile must be set before retrieving profile definitions")
    if current_profile not in PROFILES:
        raise Exception("Selected profile (%s) not in supported profile list" % current_profile)
    if def_name not in PROFILES[current_profile]:
        raise Exception("Selected def (%s) not present in selected profile" % def_name)
    return PROFILES[current_profile][def_name]
