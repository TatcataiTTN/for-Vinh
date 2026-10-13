"""Dựng file .drawio bằng Python (theo skill drawio-architecture-diagrams): dải ngang, palette chuẩn, render CLI ra PNG."""
import os, subprocess, html
PAL = {'blue': ('#dae8fc', '#6c8ebf'), 'yellow': ('#fff2cc', '#d6b656'), 'green': ('#d5e8d4', '#82b366'), 'red': ('#f8cecc', '#b85450'),
       'purple': ('#e1d5e7', '#9673a6'), 'orange': ('#ffe6cc', '#d79b00'), 'gray': ('#f5f5f5', '#666666'), 'dark': ('#1f4e8c', '#14325a')}
class D:
    def __init__(self, w=1000, h=600):
        self.w, self.h = w, h; self.cells = []; self.n = 2
    def _id(self): self.n += 1; return f'n{self.n}'
    def box(self, x, y, w, h, text, color='blue', size=16, bold=False, shape='rounded=1', font='PT Sans', fcolor=None, extra=''):
        fill, stroke = PAL[color]; i = self._id()
        fc = fcolor or ('#ffffff' if color == 'dark' else '#1d2433')
        st = f'{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={size};fontFamily={font};fontColor={fc};{"fontStyle=1;" if bold else ""}arcSize=12;strokeWidth=2;{extra}'
        v = html.escape(text, quote=True).replace('\n', '&#10;')
        self.cells.append(f'<mxCell id="{i}" value="{v}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i
    def text(self, x, y, w, h, text, size=16, bold=False, color='#1d2433', align='center'):
        i = self._id(); v = html.escape(text, quote=True).replace('\n', '&#10;')
        st = f'text;html=1;whiteSpace=wrap;align={align};verticalAlign=middle;fontSize={size};fontFamily=PT Sans;fontColor={color};{"fontStyle=1;" if bold else ""}'
        self.cells.append(f'<mxCell id="{i}" value="{v}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i
    def edge(self, a, b, label='', color='#1f4e8c', size=14, dashed=False, exit=None, entry=None):
        i = self._id(); v = html.escape(label, quote=True)
        st = f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=2;strokeColor={color};fontSize={size};fontFamily=PT Sans;labelBackgroundColor=#ffffff;{"dashed=1;" if dashed else ""}'
        if exit: st += f'exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;'
        if entry: st += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
        self.cells.append(f'<mxCell id="{i}" value="{v}" style="{st}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    def save(self, path, png=None, scale=2):
        xml = f'<mxfile host="app.diagrams.net"><diagram name="p1" id="d1"><mxGraphModel dx="{self.w}" dy="{self.h}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(self.cells) + '</root></mxGraphModel></diagram></mxfile>'
        os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w', encoding='utf-8').write(xml)
        import xml.etree.ElementTree as ET; ET.parse(path)
        if png:
            r = subprocess.run(['drawio', '--export', '--format', 'png', '--scale', str(scale), '--border', '12', '--output', png, path], capture_output=True, text=True, timeout=180)
            if r.returncode != 0: print(r.stderr[-400:])
