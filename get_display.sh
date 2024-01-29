#!/bin/bash
# Returns the DISPLAY value of the first XWindow session found. This is useful
# to start a graphical application from a SSH terminal and have the UI open on
# a separate display session, say a Chrome Remote Desktop.
#
# Sample usage:
# - Start a Chrome Remote Desktop session.
# - Open an SSH terminal
# - Start application by doing:
#   $ DISPLAY=$(get_display.sh) out/Debug/content_shell

ls /tmp/.X*-lock | sed 's/\/tmp\/\.X\([[:digit:]]\+\)-lock/:\1/' | xargs -I{} sh -c 'xdpyinfo -display {} &>/dev/null && echo {}' 2>/dev/null | head -q -n 1
