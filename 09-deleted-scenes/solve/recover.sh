#!/usr/bin/env bash
# Deleted Scenes - recover deleted files from an ext4 image with debugfs (read-only, safe to run)
IMG=${1:-../files/chall.img}

echo "## what the filesystem still lists (-d also shows deleted names; their inode shows as <0>)"
debugfs -R "ls -d -l /home/intern" "$IMG" 2>/dev/null

echo
echo "## inodes that were deleted but not wiped"
debugfs -R "lsdel" "$IMG" 2>/dev/null

echo
echo "## contents of every deleted inode"
for ino in $(debugfs -R "lsdel" "$IMG" 2>/dev/null | awk '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {print $1}'); do
  echo "--- inode $ino"
  debugfs -R "cat <$ino>" "$IMG" 2>/dev/null
done
