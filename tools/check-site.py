#!/usr/bin/env python3
"""Check local rendered pages, assets and fragments without following external URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import sys
root=Path(__file__).resolve().parents[1]/'www'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  for key in ('href','src'):
   if a.get(key):self.links.append(a[key])
pages={}
for p in root.rglob('*.html'):
 parser=Page();parser.feed(p.read_text());pages[p.resolve()]=parser
errors=[]
if not pages:errors.append('No rendered HTML; run the build first')
for p,data in pages.items():
 for link in data.links:
  u=urlsplit(link)
  if u.scheme or u.netloc or not u.path and not u.fragment:continue
  target=(root/u.path.lstrip('/') if u.path.startswith('/') else p.parent/u.path).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.name}: missing {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p.name}: missing fragment {link}')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS {len(pages)} rendered pages: local links, assets and fragments')
