from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'_site'
out.mkdir(exist_ok=True)
shutil.copytree(root/'site',out,dirs_exist_ok=True)
shutil.copytree(root/'releases/v2.1',out/'releases/v2.1',dirs_exist_ok=True)
(out/'.nojekyll').write_text('')
