from importlib.metadata import version

def get_version():
    return version('pythorhead')

from pythorhead.lemmy import Lemmy

