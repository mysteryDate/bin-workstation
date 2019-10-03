#!/usr/bin/env python3
import os, re, subprocess

def command_to_string(cmd):
  return subprocess.run(
    cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")

def get_servers():
  process_string = command_to_string(["pgrep", r"\bwebfsd"])
  PIDs = [int(x) for x in re.findall(r"\d{3,8}", process_string)]

  result = []
  for x in PIDs:
    p = command_to_string(["cat", "/proc/{}/cmdline".format(x)])
    p = p.split("-p\x00")[1].split("\x00")[0]
    f = command_to_string(["pwdx", "{}".format(x)])
    f = f.split("aaronhk/")[1].rstrip("\n")
    f = f.replace("chrome/src/third_party/blink", "BLINK")
    f = f.replace("chrome/src/third_party", "THIRD_PARTY")
    f = f.replace("chrome/src", "CS")
    result.append((int(p), f))

  result.sort(key=lambda x:x[0])
  return result

servers = get_servers()
print("\n  Port\t| Folder")
print("-------------------------------------------------")
for s in servers:
  print("  {p}\t| {f}".format(p=s[0], f=s[1]))
print("")

# From wwebfsd
"""
IFS=$'\012'

for l in `pgrep '\bwebfsd'`; do
  PID=`echo "$l" | cut -d' ' -f 1`
  CMDLINE=`cat /proc/$PID/cmdline | tr '\0' ' '`
  PCWD=`pwdx $PID | cut -d: -f 2`
  PCWD=`printf "%-40s" "$PCWD"`
  echo -e "$PID $PCWD $CMDLINE"
done
"""