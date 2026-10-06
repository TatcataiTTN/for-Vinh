"""Trang 'Phát triển': chuyển docs/DEVELOPMENT.md sang HTML bằng pandoc."""
import os, subprocess
from helpers import *

def body():
    md = os.path.join(ROOT, 'NLP-work', 'docs', 'DEVELOPMENT.md')
    h = subprocess.run(['pandoc', md, '-f', 'markdown', '-t', 'html', '--wrap=none'], capture_output=True, text=True, check=True).stdout
    h = h.replace('<table>', '<div class="tbl-wrap"><table>').replace('</table>', '</table></div>').replace('<pre class="', '<pre class="src ').replace('<pre>', '<pre class="src">')
    return '<p class="tag">PHÁT TRIỂN</p>' + h
