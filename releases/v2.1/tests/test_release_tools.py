from pathlib import Path
import hashlib,json
from verify_release import verify
from reference.check_web import audit

def fixture(root):
    (root/'release').mkdir();(root/'one.txt').write_text('one')
    h=hashlib.sha256((root/'one.txt').read_bytes()).hexdigest()
    (root/'release/MANIFEST.json').write_text(json.dumps({'files':[{'path':'one.txt','sha256':h,'bytes':3}]}))
    mh=hashlib.sha256((root/'release/MANIFEST.json').read_bytes()).hexdigest()
    (root/'release/SHA256SUMS.txt').write_text(f'{h}  one.txt\n{mh}  release/MANIFEST.json\n')

def test_hash_inventory_matches(tmp_path):fixture(tmp_path);assert verify(tmp_path)['status']=='PASS'
def test_tampered_file_rejected(tmp_path):fixture(tmp_path);(tmp_path/'one.txt').write_text('two');assert verify(tmp_path)['status']=='FAIL'
def test_missing_file_rejected(tmp_path):fixture(tmp_path);(tmp_path/'one.txt').unlink();assert verify(tmp_path)['status']=='FAIL'
def test_extra_file_rejected(tmp_path):fixture(tmp_path);(tmp_path/'two.txt').write_text('extra');assert verify(tmp_path)['status']=='FAIL'
def test_parent_path_rejected(tmp_path):fixture(tmp_path);(tmp_path/'release/SHA256SUMS.txt').write_text('0'*64+'  ../outside\n');assert verify(tmp_path)['status']=='FAIL'
def test_duplicate_hash_entry_rejected(tmp_path):
    fixture(tmp_path);p=tmp_path/'release/SHA256SUMS.txt';p.write_text(p.read_text()+p.read_text());assert verify(tmp_path)['status']=='FAIL'
def test_local_link_resolves(tmp_path):
    (tmp_path/'index.html').write_text('<a href="other.html#head">go</a>');(tmp_path/'other.html').write_text('<h1 id="head">Hi</h1>');assert audit(tmp_path)['status']=='PASS'
def test_missing_anchor_rejected(tmp_path):
    (tmp_path/'index.html').write_text('<a href="#absent">go</a>');assert audit(tmp_path)['status']=='FAIL'
def test_missing_local_file_rejected(tmp_path):
    (tmp_path/'index.html').write_text('<a href="absent.html">go</a>');assert audit(tmp_path)['status']=='FAIL'
