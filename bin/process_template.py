"""update_html_file.py

update templates block in html files.
by Kei Onimaru <otegami@devel.keys.jp>
"""

from datetime import datetime, timezone, timedelta
import glob
import json
import logging
import os
import re
from typing import List, Dict, Any, AnyStr, Optional, Match

from jinja2 import Template, Environment, DictLoader


class Jinja2TemplateProcessor:
    DEFAULT_HTML_PATH = './htdocs'
    DEFAULT_TMPL_PATH = './templates'
    DEFAULT_TMPL_CONF_FILE = './templates/template_items.json'

    def __init__(self, **kwargs):
        path_prefix: str = kwargs.get('path_prefix', '')
        self._paths: Dict[str, str] = {
            'html': os.path.join(path_prefix, self.DEFAULT_HTML_PATH),
            'jinja': os.path.join(path_prefix, self.DEFAULT_TMPL_PATH)
        }
        self._jinja_env: Environment
        self._templates: Dict[str, str] = dict()
        self._configure: Dict[str, Any] = dict()

    def _record_timestamp(self, url_path) -> str:
        tz_jst = timezone(timedelta(hours=9), 'JST')
        dt_now = datetime.now(tz_jst).isoformat(timespec='seconds')
        return F'<!-- {url_path}: updated at {dt_now} -->'

    def _render(self, url_path: str, html_file: str) -> List[str]:
        lines: List[str] = list()
        try:
            pass
        except:
            lines.append('RENDERING ERROR')
        return lines

    def _apply_each(self, url_path: str, input_lines: str) -> List[str]:
        within_tmpl_block = False
        output_lines: List[str] = list()
        match: Optional[Match[str]]
        requested_tmpl_name: str
        for line in input_lines:
            if within_tmpl_block:
                if ' /template ' in line:
                    output_lines.append(line)
                    within_tmpl_block = False
            else:
                output_lines.append(line)
                match = re.search(r' template: (\w+)', line)
                if match:
                    tmpl_name = match.group(1)
                    output_lines += self._render(url_path, tmpl_name)
                    within_tmpl_block = True
        output_lines.append(self._record_timestamp(url_path))
        return output_lines

    def _enum_files(self, ext: str, file_path: str = '') -> List[str]:
        if not file_path:
            file_path = self._paths[ext]
        file_list: List[str] = glob.glob(file_path+F'/**/*.{ext}', recursive=True)
        if not file_list:
            logging.error(F'No "{ext}" files in path: "{file_path}"')
        return file_list

    def apply(self, file_path: str = '') -> bool:
        for html_file in self._enum_files('html'):
            url_path = html_file.replace(file_path, '')
            ## taking backup
            with open(html_file, 'r') as fpr:
                output_lines = self._apply_each(url_path, fpr.read())
                with open(html_file, 'w') as fpw:
                    fpw.writelines(output_lines)
            ## end process (remove backup, and etc.)
        return True

    def load_templates(self, file_path: str = '') -> bool:
        for tmpl_file in self._enum_files('jinja'):
            with open(tmpl_file, 'r') as fpi:
                tmpl_name = os.path.basename(tmpl_file)
                self._templates[tmpl_name] = fpi.read()
        self._jinja_env = Environment(
            loader=DictLoader(self._templates),
            trim_blocks=True,
            lstrip_blocks=True
        )
        return True

    def configure(self, config_file: str = '') -> bool:
        if not config_file:
            config_file = self.DEFAULT_TMPL_CONF_FILE
        try:
            with open(config_file, 'r') as fpi:
                self._configure = json.load(fpi)
        except OSError as err:
            logging.exception(F'OS Error: file="{config_file}".', err.args)
            return False
        return True


def class_runner():
    """Class Runner

    create instance, and run methods of that for class(es) in this file.
    """
    j2tp = Jinja2TemplateProcessor(
        path_prefix=''
    )
    j2tp.configure()
    j2tp.load_templates()
    j2tp.apply()

if __name__ == '__main__':
    class_runner()
