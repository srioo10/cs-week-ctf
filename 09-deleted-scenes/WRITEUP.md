# Deleted Scenes

Forensics · 250 points · 0 solves

Flag: `CLUB{ext4_j0urnal_n3v3r_f0rg3ts}`

> Our intern wiped flag.txt from this disk image and swears it's gone for good. Is it? Careful though, not everything that looks like a flag is one.

`chall.img` is a 16 MB disk image:

```
$ file chall.img
chall.img: Linux rev 1.0 ext4 filesystem data ... volume name "backup" (extents)
```

Deleting a file on ext4 removes its directory entry and marks its blocks as free. The data stays on disk until something overwrites it.

## Recovering the file

`debugfs` reads ext2/3/4 filesystems without mounting them. Start by looking at the intern's home directory:

```
$ debugfs -R "ls -l /home/intern" chall.img
```

It has `junk.b64`, `todo.txt` and `notes.txt`. `todo.txt` says:

```
- clean up /home
- delete flag.txt (done!!)
- ask about lunch
```

Adding `-d` to `ls` lists deleted entries too:

```
$ debugfs -R "ls -d -l /home/intern" chall.img
```

Two deleted names show up, both with inode `<0>`: `old_flag.txt` and `flag.txt`. The names survived, but they no longer point to an inode. The hint covers this step: "Deleting a file doesn't zero the data. Look at what the filesystem keeps track of."

`lsdel` lists deleted inodes, and `cat` with an inode number reads them back:

```
$ debugfs -R "lsdel" chall.img
Inode  Owner  Mode    Size  ...
   15      0 100644     27
   19      0 100644     33

$ debugfs -R "cat <15>" chall.img
CLUB{check_maybe_its_fl4g}
$ debugfs -R "cat <19>" chall.img
CLUB{ext4_j0urnal_n3v3r_f0rg3ts}
```

## Which one is real

Both are flag-shaped, which is what the warning in the description is about. The challenge asks about `flag.txt`, so you have to work out which inode belonged to it.

Inodes in this image were allocated in creation order. Counting through the directory: `intern` is 14, then 15, `junk.b64` is 16, `todo.txt` 17, `notes.txt` 18, then 19. The two gaps are the deleted files. `old_flag.txt` comes first in the listing and is inode 15; `flag.txt` comes last and is inode 19. So the flag is inode 19's content, and inode 15 (`check_maybe_its_fl4g`) is the decoy.

`solve/recover.sh` runs these commands and prints both files.

## Shortcuts that don't finish the job

`strings chall.img | grep CLUB` finds both strings at once, but it can't tell you which belongs to `flag.txt`. Only the filesystem metadata answers that.

`junk.b64` is 27 KB of base64 that decodes to 20,000 random bytes with no flag in them.

The flag mentions the journal, and ext4's journal can hold old copies of metadata that help with recovery. In this image the journal is empty, so the deleted inodes were enough.

## Notes

Tools worth having for this kind of work: `debugfs`, `extundelete`, `photorec`, and The Sleuth Kit (`fls`, `icat`). Real secure deletion means overwriting the data or encrypting it from the start.

Nobody solved it during the event.
