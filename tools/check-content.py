#!/usr/bin/env python3
"""Check the curated workshop offline; never accesses clusters or credentials."""
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1]/'content/modules/ROOT';errors=[]
files=list(root.rglob('*.adoc'))
for f in files:
 text=f.read_text()
 for family,target in re.findall(r'(xref|include)::?([^\s\[]+)\[',text):
  if target.startswith(('http:','https:')):continue
  if '$' in target:
   kind,name=target.split('$',1);folder={'attachment':'attachments','partial':'partials','image':'images'}.get(kind)
   if not folder:errors.append(f'{f.name}: unknown family {kind}');continue
  else:folder,name='pages',target
  if not (root/folder/name.split('#')[0]).is_file():errors.append(f'{f.name}: missing {target}')
 if re.search(r'\[[^\]]+\]\([^)]+\)',text):errors.append(f'{f.name}: unconverted Markdown link')
 if f.name.startswith('module-') and '09-provisioning' not in f.name:
  for expected in ['Objective','Expected','Fallback','Checkpoint','Clean up']:
   if expected.lower() not in text.lower():errors.append(f'{f.name}: missing {expected}')
for f in (root/'attachments').iterdir():
 if f.suffix not in ('.yaml','.yml'):errors.append(f'Unexpected attachment: {f.name}')
 if re.search(r'^kind:\s*Secret\s*$',f.read_text(),re.M):errors.append(f'Credential-bearing attachment forbidden: {f.name}')
 if re.search(r'(?i)(BEGIN .*PRIVATE KEY|ocmClientSecret|aws_secret_access_key)',f.read_text()):errors.append(f'Sensitive field in attachment: {f.name}')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS {len(files)} AsciiDoc sources: local references, module structure, attachment hygiene')
