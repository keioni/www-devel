
import json
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader

def main():
    env = Environment(loader=FileSystemLoader('templates/'))
    tmpl = env.get_template('common_header.html')

    with open('templates/template_items.json') as fpjson:
        v = json.load(fpjson)
    items = v['navbar']['common_header']['items']
    html_lines = tmpl.render(items=items).split('\n')
    for line in html_lines:
        if not re.search(r'^ +$', line, re.MULTILINE):
            print(line)

if __name__ == '__main__':
    main()
