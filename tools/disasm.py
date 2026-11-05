"""Disassemble ATC CODE: python dis.py <app.rsrc> <seg> [start_hex] [count] | python dis.py <app.rsrc> find <trapword_hex> [before] [after]"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rfork import raw_fork, resources
import capstone
src = open(r'C:/Users/Drew0/Claude/Falcon_Sierra_PC/decomp/name_traps.py').read()
ns = {}; exec(src.split('def name_for')[0], ns); OS, TB = ns['OS'], ns['TB']
EXTRA = {0xA862:'ForeColor',0xA863:'BackColor',0xA869:'FixRatio',0xA86F:'OpenPort',0xA870:'LocalToGlobal',0xA871:'GlobalToLocal',
 0xA87D:'ClosePort',0xA898:'GetPenState',0xA899:'SetPenState',0xA8BF:'PaintArc',0xA8E1:'InsetRgn',0xA8E2:'EmptyRgn',0xA8E9:'RectInRgn',
 0xA8FD:'PrGlue',0xA8FE:'InitFonts',0xA906:'NewString',0xA909:'CalcVis',0xA936:'DeleteMenu',0xA938:'HiliteMenu',0xA94C:'FlashMenuBar',
 0xA950:'CountMItems',0xA959:'MoveControl',0xA95C:'SizeControl',0xA961:'GetMinCtl',0xA962:'GetMaxCtl',0xA964:'SetMinCtl',0xA965:'SetMaxCtl',
 0xA97E:'SelIText',0xA998:'UseResFile',0xA9B1:'CreateResFile',0xA9B8:'GetPattern',0xA9BA:'GetString',0xA9BF:'GetMenu',0xA9E1:'HandToHand',
 0xA9EA:'Pack3',0xA9EB:'Pack4',0xA9EE:'Pack7',0xAA45:'NewCWindow',0xAA46:'GetNewCWindow',0xAA48:'GetCWMgrPort'}
OSX = {0x32:'FlushEvents',0x36:'MoreMasters',0x49:'HPurge',0x4A:'HNoPurge',0x4B:'SetGrowZone',0x55:'StripAddress',0x60:'HFSDispatch',
 0x63:'MaxApplZone',0x64:'MoveHHi',0x90:'SysEnvirons',0x46:'GetTrapAddress'}
def tname(w):
    if w < 0xA800: return OSX.get(w & 0xFF) or OS.get(w & 0xFF, '?')
    return EXTRA.get(w & 0xFBFF) or TB.get(w, TB.get(w & 0xFBFF, '?'))
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
