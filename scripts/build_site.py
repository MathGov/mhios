from pathlib import Path
import shutil
from lxml import html, etree
root=Path(__file__).resolve().parents[1]
out=root/'_site'
out.mkdir(exist_ok=True)
shutil.copytree(root/'site',out,dirs_exist_ok=True)
shutil.copytree(root/'releases/v2.1',out/'releases/v2.1',dirs_exist_ok=True)
# Generate an accessible reading projection without editing the frozen package.
source=root/'releases/v2.1/docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.html'
doc=html.fromstring(source.read_text(encoding='utf-8'))
doc.set('lang','en');doc.set('xml:lang','en')
head=doc.find('head');body=doc.find('body')
for link in head.xpath('./link[@rel="stylesheet"]'):
    link.set('href','../releases/v2.1/web/reading.css')
head.find('title').text='Read MHIOS v2.1 | Complete standard'
etree.SubElement(head,'link',rel='canonical',href='https://mathgov.github.io/mhios/read/')
etree.SubElement(head,'meta',name='description',content='Complete MHIOS v2.1 reading projection, pinned to Core v13.0 Release I and SGP v8.8. Original source and editable downloads remain available.')
style=etree.SubElement(head,'style')
style.text='html{overflow-wrap:anywhere}body{box-sizing:border-box;width:100%;min-width:0}nav ul{padding-left:1.1rem}table{max-width:100%;table-layout:fixed}.table-scroll{overflow-x:auto;max-width:100%}.table-scroll table{display:table;min-width:36rem}main{min-width:0} .publication-note{padding:1rem;background:#fbf7ee;border-left:4px solid #b8851f} .table-scroll:focus-visible{outline:3px solid #986800}h1{overflow-wrap:anywhere}'
notice=html.fragment_fromstring('<div class="publication-note"><a href="../">← MHIOS publication and downloads</a><p>Hosted reading projection of the unchanged v2.1 standard. Page language and responsive table presentation were improved; semantic text is unchanged. Tables scroll horizontally on small screens and can be focused with the keyboard.</p></div>')
body.insert(0,notice)
toc=body.find('nav')
if toc is not None:
    toc.set('aria-label','Standard contents')
    details=etree.Element('details');summary=etree.SubElement(details,'summary');summary.text='Contents — jump to a section'
    toc.addprevious(details);details.append(toc)
main=etree.Element('main',id='standard-text')
started=False
for el in list(body):
    if el.tag=='h1' and el.get('id')=='mathgov-human-interface-and-orchestration-standard':started=True
    if started:main.append(el)
body.append(main)
skip=etree.Element('a',href='#standard-text',attrib={'class':'skip'});skip.text='Skip to standard';body.insert(0,skip)
for i,table in enumerate(main.xpath('.//table'),1):
    wrap=etree.Element('div',attrib={'class':'table-scroll','role':'region','aria-label':f'Table {i}, scroll horizontally if needed','tabindex':'0'})
    table.addprevious(wrap);wrap.append(table)
original=html.fromstring(source.read_text(encoding='utf-8')).find('body')
first=original.xpath('./h1[@id="mathgov-human-interface-and-orchestration-standard"]')[0]
nodes=list(original);start=nodes.index(first)
def tokens(s):return s.split()
assert tokens(' '.join(e.text_content() for e in nodes[start:]))==tokens(''.join(main.itertext()))
(out/'read').mkdir(exist_ok=True)
(out/'read/index.html').write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode'),encoding='utf-8')
(out/'.nojekyll').write_text('')
