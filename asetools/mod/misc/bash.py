import sys
import subprocess

def gzip_file(filename):
    subprocess.check_call(['gzip', filename])

