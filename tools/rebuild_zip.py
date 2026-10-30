"""Portable standard-ZIP packager. No symlinks, ZIP64, encryption or exotic compression.
Usage: python tools/rebuild_zip.py --output C:/path/NaikReady_FIXED.zip
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
SKIP={'node_modules','.venv','venv','__pycache__','.pytest_cache','runtime','.git','dist'}

def files_for(root):
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if SKIP.intersection(rel.parts) or p.suffix in {'.pyc','.tsbuildinfo'}:continue
        if p.is_symlink():raise ValueError(f'Symlink not permitted: {rel}')
        if p.is_file():yield p,rel

def rebuild(root,output):
    entries=list(files_for(root))
    names=[rel.as_posix() for _,rel in entries]
    assert len(names)==len(set(n.lower() for n in names)), 'Case-colliding paths'
    for name in names:
        assert not any(c in name for c in '<>:"\\|?*'),name
        assert not any(part.endswith((' ','.')) for part in PurePosixPath(name).parts),name
        assert len(root.name+'/'+name)<240,name
    # Build off the final pathname. Publish only after the central directory is closed,
    # flushed and independently validated; readers can never see a half-written ZIP.
    with tempfile.TemporaryDirectory(prefix='naikready-package-') as tmp:
        work=Path(tmp)/'complete.zip'
        with work.open('w+b') as file:
            with zipfile.ZipFile(file,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=False) as z:
                for path,rel in entries:
                    info=zipfile.ZipInfo(root.name+'/'+rel.as_posix(),date_time=(2026,10,29,0,0,0))
                    info.create_system=0
                    info.external_attr=0x20
                    info.compress_type=zipfile.ZIP_DEFLATED
                    z.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
            file.flush();os.fsync(file.fileno())
        with zipfile.ZipFile(work) as z:
            assert z.testzip() is None
            assert len(z.infolist())==len(entries)
            assert all(i.extract_version<=20 and not i.flag_bits&1 for i in z.infolist())
        output.parent.mkdir(parents=True,exist_ok=True)
        # Copy to a sibling staging file, fsync, then atomically replace destination.
        staging=output.with_suffix('.complete.tmp')
        with work.open('rb') as src,staging.open('wb') as dest:
            while block:=src.read(1024*1024):dest.write(block)
            dest.flush();os.fsync(dest.fileno())
        staging.replace(output)
    with zipfile.ZipFile(output) as z:assert z.testzip() is None
    return {'file':str(output),'size_bytes':output.stat().st_size,'files':len(entries),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.resolve().is_relative_to(ROOT):raise ValueError('Output ZIP must be outside the project folder.')
    print(json.dumps(rebuild(ROOT,args.output.resolve())))
