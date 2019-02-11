import os, re, subprocess

STARTING_PORT = 5000

def command_to_string(cmd):
  return subprocess.run(
    cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")

process_string = command_to_string(["pgrep", r"\bwebfsd"])
PIDs = [int(x) for x in re.findall(r"\d{3,8}", process_string)]

occupied_ports = []
for pid in PIDs:
  proc = command_to_string(["cat", "/proc/{}/cmdline".format(pid)])
  proc = proc.replace("\x00", " ")
  port_number = re.findall(r"\d{3,8}", proc)[0]
  occupied_ports.append(int(port_number))

occupied_ports.sort()
new_port = str(occupied_ports[-1] + 1)
subprocess.run(["webfsd", "-p", new_port, "-e0"])

current_directory = os.getcwd()
output_string = "Started new server at {d} using port {p}".format(d=current_directory, p=new_port)
print(output_string)
