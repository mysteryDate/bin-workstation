import subprocess
import time
import threading
import signal
import re
import os
import sys
import argparse

def modify_line_in_file(filename, pattern, replacement):
  """Opens a file, finds a line matching a pattern, modifies it, and saves the changes.

  Args:
    filename: The path to the file.
    pattern: The regular expression pattern to search for.
    replacement: The replacement text for the matched line.
  """

  try:
    with open(filename, 'r') as file:
      contents = file.readlines()

    with open(filename, 'w') as file:
      for line in contents:
        if re.search(pattern, line):
          modified_line = line.replace(re.search(r"\d+", line).group(), replacement)
          file.write(modified_line)
        else:
          file.write(line)

  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")


def focus_vscode():
  """
  Use xdotool to focus a vscode window
  """
  def parse_int_list(string_list):
    parsed_ints = []
    for string in string_list:
      try:
        parsed_int = int(string)
        parsed_ints.append(parsed_int)
      except ValueError:
        pass
    return parsed_ints

  proc = subprocess.run(['xdotool', 'getactivewindow'],
              capture_output=True, text=True)
  active_window_PID = int(proc.stdout)
  proc = subprocess.run(['xdotool', 'search', '--onlyvisible',
               '--class', 'code'], capture_output=True, text=True)
  vscode_window_PIDs = parse_int_list(proc.stdout.split('\n'))
  for PID in vscode_window_PIDs:
    if PID != active_window_PID:
      subprocess.run(['xdotool', 'windowactivate', str(PID)])

def execute_and_capture_stderr(command, remote):
  """Executes a Unix command and captures stderr output in real-time.

  Args:
    command: The Unix command to execute as a string.
  """

  process = subprocess.Popen(
    command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    preexec_fn=os.setsid  # Create a new process group
  )

  # Handle Ctrl+C (SIGINT)
  def signal_handler():
    print("Interrupt received, terminating the process...")
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Kill the process group
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)

  launch_filepath = ".vscode/launch.json"
  match_pattern = '"processId": "\d+"'

  # Thread to read stderr and print in real-time
  def read_stderr():
    PID_counter = 0 # We want the 2nd PID
    for line in iter(process.stderr.readline, ''):
      print(line, end='')
      search = re.search("Renderer \(\d+\)", line)
      if (search):
        PID = int(re.search("\d+", search.group()).group())
        print("found process id {}".format(PID))
        PID_counter += 1
        if (PID_counter == 2):
          print("replacing processId in {} with: {}".format(launch_filepath, PID))
          modify_line_in_file(launch_filepath, match_pattern, str(PID))
          if not remote:
            # Start the debugger
            print("Sending F5 to vscode to start debugger")
            focus_vscode()
            subprocess.run(['xdotool', 'key', 'F5'])

  stderr_thread = threading.Thread(target=read_stderr)
  stderr_thread.start()
  process.wait()  # Wait for the process to complete
  stderr_thread.join()  # Wait for the stderr thread to finish


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("--remote", action='store_true',
                      help="Is this a remote session?")

  parser.add_argument("site", help="The website to load.", default="", nargs='?')

  args = parser.parse_args()

  os.chdir(os.path.join(os.path.expanduser("~"), "chrome", "src"))

  command = "{} out/Debug/content_shell --no-sandbox --renderer-startup-dialog \
      --enable-experimental-web-platform-features {}".format(
        "DISPLAY=\":20\"" if args.remote else "", args.site)

  print("Executing command:\n{}".format(command))
  execute_and_capture_stderr(command, args.remote)

if __name__ == "__main__":
  main()
