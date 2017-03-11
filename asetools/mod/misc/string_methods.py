

def get_shared_prefix(string1, string2, strip_chars=[]):
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




