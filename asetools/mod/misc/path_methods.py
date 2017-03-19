"""
Miscellaneous path methods to help execute methods throughout the asetools package.
"""

from os.path import basename


def get_shared_prefix(string1, string2, strip_chars=None, base=False):
    """
    Returns the shared prefix of two strings, useful for getting the shared prefix of two paths.
    :param string1: The first string of interest
    :param string2: The second string of interest
    :param strip_chars: A list of characters to strip from the resulting shared prefix
    :param base: If a path, take the basename(path) of the shared prefix and return it.
    :return: The shared prefix of the two strings
    """
    if strip_chars is None:
        strip_chars = []
    if base:
        string1 = basename(string1)
        string2 = basename(string2)

    string1 = list(string1)
    string2 = list(string2)

    out_string = ''
    for c1, c2 in zip(string1, string2):
        if c1 == c2:
            out_string += c1
        else:
            break

    for char in strip_chars:
        out_string = out_string.strip(char)

    return out_string





