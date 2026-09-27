#!/usr/bin/env python3
"""Render a nonsecret local guide profile. Never contacts a cluster."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS={
 'profile-name':('Workshop name','My fleet workshop'),
 'source-cluster':('Source ManagedCluster name',''),
 'destination-cluster':('Destination ManagedCluster name',''),
 'hub-context':('Hub CLI context name',''),
 'hub-api':('Hub API URL (no credentials)',''),
 'hub-console':('Hub console URL (no credentials)',''),
 'source-region':('Actual source region',''),
 'destination-region':('Actual destination region',''),
 'cluster-set':('Prepared ManagedClusterSet name',''),
}
def validate(values):
 if set(values)!=set(FIELDS):raise ValueError('Profile must contain exactly the documented nonsecret fields')
 for key,value in values.items():
  if not isinstance(value,str) or not value.strip() or len(value)>180 or any(c in value for c in '\n\r{}[]<>\\'):raise ValueError('Invalid value for '+key)
  if key in ('source-cluster','destination-cluster','cluster-set') and not re.fullmatch(r'[a-z0-9]([a-z0-9.-]*[a-z0-9])?',value):raise ValueError('Expected a Kubernetes resource name for '+key)
  if key in ('hub-api','hub-console') and not re.fullmatch(r'https://[a-zA-Z0-9.-]+(?::[0-9]+)?/?',value):raise ValueError('Expected plain HTTPS origin, without path, query or credentials: '+key)
 if values['source-cluster']==values['destination-cluster']:raise ValueError('Choose two distinct ManagedCluster identities')
 return values

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--profile',type=Path,help='Existing JSON profile instead of prompts');parser.add_argument('--validate',action='store_true',help='Validate only; write nothing');args=parser.parse_args()
 try:
  if args.profile:values=json.loads(args.profile.read_text())
  else:
   print('Guide values only. Do not enter credentials. No cluster changes will be made.')
   values={}
   for key,(label,default) in FIELDS.items():values[key]=input(label+(f' [{default}]' if default else '')+': ').strip() or default
  validate(values)
  if args.validate:print('Profile valid; no files written.');return
  base=(ROOT/'antora-playbook.yml').read_text();marker='  attributes:\n';assert base.count(marker)==1
  generated=base.replace(marker,marker+''.join('    '+k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in values.items()))
  (ROOT/'profiles/local.json').write_text(json.dumps(values,indent=2)+'\n');(ROOT/'antora.local.yml').write_text(generated)
  print('Wrote ignored profiles/local.json and antora.local.yml. Documentation only; preparation configuration unchanged.')
 except (ValueError,OSError,EOFError) as e:parser.error(str(e))
if __name__=='__main__':main()
