"""update_html_file.py

update templates block in html files.
by Kei Onimaru <otegami@devel.keys.jp>
"""

import glob
import json
import os
import re
from typing import List, Dict, Any, Optional, Match

from jinja2 import Template, Environment, DictLoader


class Jinja2TemplateProcessor:
    DEFAULT_HTML_PATH = './htdocs'
    DEFAULT_TMPL_PATH = './templates'

    def __init__(self, path_prefix: str = ''):
        self._html_path = os.path.join(path_prefix, self.DEFAULT_HTML_PATH)
        self._tmpl_path = os.path.join(path_prefix, self.DEFAULT_TMPL_PATH)
        self._jinja_env: Environment
        self._templates: Dict[str, str] = dict()
        self._configure: Dict[str, Any] = dict()

    def _render(self, url_path: str, html_file: str) -> Optional[List[str]]:
        return list()

    def _apply_each(self, url_path: str, input_lines: str) -> List[str]:
        within_tmpl_block = False
        output_lines: List[str] = list()
        match: Optional[Match[str]]
        requested_tmpl_name: str
        for line in input_lines:
            if within_tmpl_block:
                match = re.search(r'/template ', line)
                if match:
                    requested_tmpl_name = match.group(1)
                    output_lines.append(line)
                    within_tmpl_block = False
            else:
                match = re.search(r'template: (\w+)', line)
                if match:
                    requested_tmpl_name = match.group(1)
                    tmpl_lines = self._render(url_path, requested_tmpl_name)
                    if tmpl_lines:
                        output_lines += tmpl_lines
                    within_tmpl_block = True
                output_lines.append(line)
        return output_lines

    def apply(self, file_path: str = '') -> bool:
        file_list: List[str]
        if not file_path:
            file_path = self._html_path
        file_list = glob.glob(file_path+'/**/*.html', recursive=True)
        for html_file in file_list:
            url_path = html_file.replace(file_path, '')
            ## taking backup
            with open(html_file, 'r') as fpr:
                output_lines = self._apply_each(url_path, fpr.read())
                with open(html_file, 'w') as fpw:
                    fpw.writelines(output_lines)
            ## end process (remove backup, and etc.)
        return True

    def load_templates(self, file_path: str = ''):
        if not file_path:
            file_path = self._tmpl_path
        file_list = glob.glob(file_path+'/**/*.jinja', recursive=True)
        for tmpl_file in file_list:
            with open(tmpl_file, 'r') as fpi:
                tmpl_name = os.path.basename(tmpl_file)
                self._templates[tmpl_name] = fpi.read()
        self._jinja_env = Environment(
            loader=DictLoader(self._templates),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def configure(self, config_file: str = ''):
        if not config_file:
            config_file = self._tmpl_path + './template_items.json'
        with open(config_file, 'r') as fpi:
            self._configure = json.load(fpi)


def class_runner():
    """Class Runner

    create instance, and run methods of that for class(es) in this file.
    """
    j2tp = Jinja2TemplateProcessor()
    j2tp.configure()
    j2tp.load_templates()
    j2tp.apply()

if __name__ == '__main__':
    class_runner()
