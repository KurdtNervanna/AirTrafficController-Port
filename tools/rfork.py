"""Resource-fork helpers for the ATC port.

  python rfork.py extract <in> <out.rsrc>   AppleDouble / MacBinary / raw -> raw resource fork
  python rfork.py list <file> [TYPE...]     list resources (optionally only some types)
"""
import struct, sys


def raw_fork(b):
    if b[:4] == b'\x00\x05\x16\x07':                       # AppleDouble
        n = struct.unpack('>H', b[24:26])[0]
        for i in range(n):
            eid, off, ln = struct.unpack('>III', b[26 + i * 12:38 + i * 12])
            if eid == 2:
                return b[off:off + ln]
        raise ValueError('AppleDouble without a resource fork')
    if len(b) > 128 and b[0] == 0 and 0 < b[1] < 64 and b[74] == 0 and b[82] == 0:   # MacBinary
        dlen, rlen = struct.unpack('>II', b[83:91])
        rs = 128 + (dlen + 127) // 128 * 128
        return b[rs:rs + rlen]
    return b


def resources(r):
    doff, moff, dlen, mlen = struct.unpack('>IIII', r[:16])
    m = r[moff:moff + mlen]
    tlo, nlo = struct.unpack('>HH', m[24:28])
    nt = struct.unpack('>H', m[tlo:tlo + 2])[0] + 1
    out = []
    for i in range(nt):
        t = m[tlo + 2 + i * 8:tlo + 6 + i * 8].decode('mac_roman')
        cnt, rlo = struct.unpack('>HH', m[tlo + 6 + i * 8:tlo + 10 + i * 8])
        for j in range(cnt + 1):
            e = m[tlo + rlo + j * 12:tlo + rlo + j * 12 + 12]
            rid, nmo = struct.unpack('>hH', e[:4])
            ro = int.from_bytes(e[5:8], 'big')
            ln = struct.unpack('>I', r[doff + ro:doff + ro + 4])[0]
            nm = '' if nmo == 0xFFFF else m[nlo + nmo + 1:nlo + nmo + 1 + m[nlo + nmo]].decode('mac_roman')
            out.append((t, rid, nm, r[doff + ro + 4:doff + ro + 4 + ln]))
    return out


if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    data = raw_fork(open(path, 'rb').read())
    if cmd == 'extract':
        open(sys.argv[3], 'wb').write(data)
        print(f'{sys.argv[3]}: {len(data)} bytes')
    elif cmd == 'list':
        want = set(sys.argv[3:])
        for t, rid, nm, b in resources(data):
            if not want or t in want:
                print(f'{t!r} {rid:6d} {len(b):7d} {nm}')
