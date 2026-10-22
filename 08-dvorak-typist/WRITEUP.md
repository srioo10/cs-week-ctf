# Dvorak Typist

Forensics · 400 points · 0 solves

Flag: `CLUB{ayooo_keyboard_capture_found}`

> We captured a USB keyboard while someone typed a secret into a terminal. Something about the keys looks off, and they made a few mistakes along the way. Recover what was actually submitted.

`keys.pcap` holds 243 packets of USB traffic, not network traffic. This was the highest-value challenge, and it's a chain of four steps. Each step is simple, but you need all four.

## 1. Find the keyboard

The capture has two devices. Device 2 sends 194 packets of 8 bytes each. Device 3 sends 49 packets of 4 bytes each, which looks like a mouse. Only device 2 is the keyboard (hint: "Not every USB packet is the keyboard"). In Wireshark, filter on `usb.device_address == 2` and add `usb.capdata` as a column.

## 2. Decode the reports

A USB keyboard sends an 8-byte HID report whenever its state changes:

| Byte | Contents |
|---|---|
| 0 | Modifier keys: `0x02` is left Shift, `0x20` is right Shift |
| 1 | Reserved |
| 2–7 | Up to six keys currently held, as usage codes |

Usage codes describe a physical key position, not a letter. `0x04` is the key in the position where QWERTY has A, `0x05` is the B position, `0x1e` is 1, `0x28` is Enter and `0x2a` is Backspace. A key that's held down appears in several reports in a row, so only count a key in the report where it first appears.

## 3. Use the right layout

Mapped through QWERTY, the keystrokes come out as:

```
IPFN-mt'lamd'g;'ndl'hs.do=<<<<<<...
```

On a Dvorak keyboard, the physical keys QWERTY labels `I P F N` produce `C L U B`. The title says Dvorak, and the hint "The key codes are physical positions" points the same way. Remap every position to its Dvorak character. For example, the QWERTY S position gives `o`, and `{` is Shift plus the QWERTY `-` position.

## 4. Replay the typing

Read straight through, with `<` for each Backspace:

```
CLUB{my_name_is_ben_dover}<<<<<<<<<<<<<<<<<<<<<<<<<<CLUBk<{ayooo_keu<ybw<oard_cl<apture_founq<d}
```

There are 31 Backspaces. The typist entered a decoy flag, `CLUB{my_name_is_ben_dover}`, deleted all 26 characters, started again, made five typos (`k`, `u`, `w`, `l`, `q`) that were each fixed with Backspace, then pressed Enter. Applying each Backspace to the text gives what was actually submitted:

```
CLUB{ayooo_keyboard_capture_found}
```

`solve/dvorak_typist.py` parses the pcap without extra libraries, keeps only device 2, maps positions through the Dvorak layout and applies the Backspaces.

## Notes

The usual mistakes were decoding device 3's 4-byte packets as keystrokes, staying on QWERTY, submitting the decoy, and counting a held key several times.

Nobody solved this one. The three hints covered the device filter, the layout and the Backspace replay.
