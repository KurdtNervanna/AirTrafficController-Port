"""Disassemble ATC CODE: python disasm.py <app.rsrc> <seg> [start_hex] [count] | python disasm.py <app.rsrc> find <trapword_hex> [before] [after]"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rfork import raw_fork, resources
import capstone
from trapnames import name as tname
rs = {(t, rid): b for t, rid, nm, b in resources(raw_fork(open(sys.argv[1], 'rb').read()))}
md = capstone.Cs(capstone.CS_ARCH_M68K, capstone.CS_MODE_M68K_020)
def lines(seg):
    b = rs[('CODE', seg)]; off = 4; out = []
    while off < len(b) - 1:
        w = struct.unpack('>H', b[off:off+2])[0]
        if 0xA000 <= w <= 0xAFFF:
            out.append((off, f'_{tname(w)} ({w:04X})')); off += 2; continue
        ins = next(md.disasm(b[off:off+10], off), None)
        if ins: out.append((off, f'{ins.mnemonic} {ins.op_str}')); off += ins.size
        else: out.append((off, f'dc.w ${w:04X}')); off += 2
    return out
if sys.argv[2] == 'find':
    w = int(sys.argv[3], 16); bef = int(sys.argv[4]) if len(sys.argv) > 4 else 8; aft = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    for seg in sorted(r for t, r in rs if t == 'CODE' and r):
        L = lines(seg)
        for i, (o, s) in enumerate(L):
            if f'({w:04X})' in s:
                print(f'--- CODE {seg} +{o:04X}')
                for o2, s2 in L[max(0, i-bef):i+aft+1]: print(f'   {o2:05X}  {s2}')
else:
    seg = int(sys.argv[2]); st = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0; n = int(sys.argv[4]) if len(sys.argv) > 4 else 100000
    for o, s in lines(seg):
        if o >= st and n > 0: print(f'{o:05X}  {s}'); n -= 1
