# Replay

Misc · 50 points · 14 solves

Flag: `CLUB{p4ck3ts_n3v3r_l13}`

> A coworker's session was captured on the network. Something was left behind. Can you find it?

This was the warm-up, and the most solved challenge of the event. You get `replay.pcap`, 110 packets of network traffic.

Open it in Wireshark and check Statistics → Conversations (or Protocol Hierarchy). There are two conversations: HTTP on port 80 and Telnet on port 23.

The HTTP one is a decoy. It serves a page for `intranet.corp.local` with an HTML comment containing `CLUB{fake_flag_keep_looking}`.

Telnet is the interesting one. It sends everything in plain text, including the password, and usually one character per packet. Right-click any Telnet packet and choose Follow → TCP Stream, and Wireshark puts the session back together:

```
Ubuntu 22.04 LTS
login: admin
Password: hunter2

Welcome, admin
$ ls
flag.txt  notes.md
$ cat flag.txt
CLUB{p4ck3ts_n3v3r_l13}
$ exit
logout
```

The coworker logged in, ran `cat flag.txt`, and the flag went across the wire in the clear.

From the command line, `tshark -r replay.pcap -q -z follow,tcp,ascii,1` prints the same stream, and `solve/replay_extract.py` rebuilds it in Python.

## Notes

Telnet, FTP and plain HTTP expose everything to anyone who can capture the traffic, which is why SSH and HTTPS replaced them. In any capture, check every conversation before trusting the first flag-shaped string.

The password, `hunter2`, is an old internet joke.
