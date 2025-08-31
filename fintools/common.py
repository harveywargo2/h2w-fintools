import os


def desktop_path():
    home = os.path.expanduser('~')

    if os.name == 'nt':
        desktop_path = os.path.join(home, 'Desktop')
    elif os.name == 'posix':
        desktop_path = os.path.join(home, 'Desktop')
    else:
        return None

    return desktop_path

