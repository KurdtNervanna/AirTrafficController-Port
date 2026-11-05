"""List the A-line traps an app's CODE uses: python traps.py <app.rsrc>"""
import struct, sys, collections, os
sys.path.insert(0, os.path.dirname(__file__))
from rfork import raw_fork, resources
import capstone
from trapnames import name
rs = resources(raw_fork(open(sys.argv[1], 'rb').read()))
md = capstone.Cs(capstone.CS_ARCH_M68K, capstone.CS_MODE_M68K_020)
tr = collections.Counter(); first = {}
for t, rid, nm, b in rs:
    if t != 'CODE' or rid == 0: continue
    off = 4
    while off < len(b) - 1:
        w = struct.unpack('>H', b[off:off+2])[0]
        if 0xA000 <= w <= 0xAFFF:
            tr[w] += 1; first.setdefault(w, (rid, off)); off += 2; continue
        ins = next(md.disasm(b[off:off+10], off), None)
        off += ins.size if ins else 2
for w in sorted(tr):
    print(f'{w:04X} {name(w):18s} {tr[w]:4d}  CODE{first[w][0]}+{first[w][1]:04X}')
