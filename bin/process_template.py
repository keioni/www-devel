import glob
import json
import os
from typing import List, Dict, Any

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

    def _apply_one(self, file_name: str, file_data: str):
        pass

    def apply(self, file_path: str = ''):
        if not file_path:
            file_path = self._html_path
        file_list = glob.glob(file_path+'/**/*.html', recursive=True)
        for html_file in file_list:
            with open(html_file, 'r') as fpi:
                self._apply_one(html_file, fpi.read())

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


if __name__ == '__main__':
    basedir = './'
    j2tp = Jinja2TemplateProcessor()
    j2tp.configure()
    j2tp.load_templates()
    j2tp.apply()
