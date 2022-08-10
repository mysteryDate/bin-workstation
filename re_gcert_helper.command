#!/bin/sh

# Helper for ensuring we have gcert by using a Terminal window to prompt for it if needed.

# This is a .command file. Invoking it using:
#   open -W -n ~/bin/re_gcert_helper.command
# This will create a new Terminal instance and a new Terminal window for the prompt.
# When gcert exits, the window and the Terminal instance will close.

# Sources:
# https://yaqs.corp.google.com/eng/q/6704876541837312
# https://stackoverflow.com/questions/989349/running-a-command-in-a-new-mac-os-x-terminal-window
# https://apple.stackexchange.com/questions/322938/close-terminal-using-exit-when-only-one-window-is-present-close-window-otherw
# https://stackoverflow.com/questions/26770568/vs-with-the-test-command-in-bash

gcert; osascript -e 'tell application "Terminal" to quit' &
