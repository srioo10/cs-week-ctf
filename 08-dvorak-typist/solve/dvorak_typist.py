# Dvorak Typist - decode USB HID keyboard reports from a usbmon capture
import struct, sys

# ---- 1. read the pcap by hand (link type 220 = USB with 64-byte "usbmon" header) -------------
def read_pcap(path):
    data = open(path, "rb").read()
    magic = data[:4]
    endian = "<" if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1") else ">"
    off = 24
    while off + 16 <= len(data):
        ts_s, ts_u, incl, orig = struct.unpack(endian + "IIII", data[off:off+16])
        yield data[off+16: off+16+incl]
        off += 16 + incl

# ---- 2. keep only the keyboard: device 2, endpoint 0x81, 8-byte reports -----------------------
reports = []
devices = {}
for pkt in read_pcap(sys.argv[1] if len(sys.argv) > 1 else "../files/keys.pcap"):
    ev_type, xfer, ep, dev = pkt[8], pkt[9], pkt[10], pkt[11]
    payload = pkt[64:]
    devices[(dev, ep)] = devices.get((dev, ep), 0) + 1
    if dev == 2 and ep == 0x81 and len(payload) == 8:
        reports.append(payload)
print("devices seen (device, endpoint): packets ->", {f"dev{d} ep{e:#x}": n for (d, e), n in devices.items()})
print(len(reports), "keyboard reports")

# ---- 3. physical key position (HID usage) -> character, assuming a Dvorak layout ---------------
qwerty_row = "abcdefghijklmnopqrstuvwxyz1234567890"      # HID usages 0x04..0x27
# what each *physical* QWERTY key produces on a Dvorak keyboard (unshifted, shifted)
dvorak_of_qwerty = {}
q_keys = "qwertyuiop[]asdfghjkl;'zxcvbnm,./-="
d_keys = "',.pyfgcrl/=aoeuidhtns-;qjkxbmwvz[]"
d_shift = '"<>PYFGCRL?+AOEUIDHTNS_:QJKXBMWVZ{}'
for qk, dk, ds in zip(q_keys, d_keys, d_shift):
    dvorak_of_qwerty[qk] = (dk, ds)

hid_to_qwerty = {}
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
    hid_to_qwerty[0x04 + i] = ch
for i, ch in enumerate("1234567890"):
    hid_to_qwerty[0x1e + i] = ch
hid_to_qwerty.update({0x2d: "-", 0x2e: "=", 0x2f: "[", 0x30: "]", 0x33: ";", 0x34: "'", 0x36: ",", 0x37: ".", 0x38: "/"})
shift_digits = dict(zip("1234567890", "!@#$%^&*()"))

def key_to_char(usage, shift):
    if usage == 0x2c: return " "
    if usage == 0x28: return "\n"
    q = hid_to_qwerty.get(usage)
    if q is None: return ""
    if q in dvorak_of_qwerty:
        base, shifted = dvorak_of_qwerty[q]
        return shifted if shift else base
    return shift_digits[q] if shift else q

# ---- 4. replay the typing, including backspace -------------------------------------------------
buf, prev = "", set()
for r in reports:
    mod, keys = r[0], set(k for k in r[2:] if k)
    shift = bool(mod & 0x22)
    for k in keys - prev:                  # newly pressed keys only
        if k == 0x2a:                      # backspace
            buf = buf[:-1]
        else:
            buf += key_to_char(k, shift)
    prev = keys
print("--- what was on screen at the end ---")
print(buf)
