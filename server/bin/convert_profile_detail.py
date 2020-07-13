
import sys
import re

def convert():
    data = sys.stdin.read()
    paragraphs = re.split(r'\n\n', data)
    for parag in paragraphs:
        lines = re.split(r'\n', parag)
        for line in lines:
            pass
