"""Check local static reading links, without following external sites or executing scripts."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if a.get('href'): self.links.append(a['href'])
        if a.get('src'): self.links.append(a['src'])
def inspect_html(path):
    p=Links();p.feed(path.read_text(encoding='utf-8'));return p

def audit(root=ROOT):
    checks=[];external=[]
    for src in sorted(root.rglob('*.html')):
        data=inspect_html(src)
        checks.append({'check':str(src.relative_to(root))+': unique IDs','pass':len(data.ids)==len(set(data.ids))})
        for ref in data.links:
            u=urlsplit(ref)
            if u.scheme or u.netloc:external.append(ref);continue
            target=(src.parent/unquote(u.path)).resolve() if u.path else src.resolve()
            ok=target.is_relative_to(root.resolve()) and target.is_file()
            if ok and u.fragment and target.suffix=='.html':ok=unquote(u.fragment) in inspect_html(target).ids
            checks.append({'check':str(src.relative_to(root))+': '+ref,'pass':ok})
    return {'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks,
            'external_links_not_verified_in_this_check':sorted(set(external)),
            'scope':'Static local files and HTML anchors only, not browser accessibility or deployed-host conformance.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();r=audit()
    if args.output:args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
