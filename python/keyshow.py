import os
import sys
import termios
import tty

# file descriptor is a smallest int that uniquely identifies a resource or a filed opened by that os process
# almost every process has stdin 0, stdout 1 and stderr 2 as the first three file descriptors
# if 0-10 exist, and 7 is closed, the next file opened will be assigned 7 as its fd because 7 is the smallest int available

fd = sys.stdin.fileno()  # which is always 0

# save the current terminal settings so we can restore them later
saved = termios.tcgetattr(fd)

# set the terminal to raw mode, which means that input is read byte-by-byte, without any processing or buffering
# which allows us to read the input as it is typed, without waiting for a newline or other special characters
tty.setraw(fd)

try:
    while True:
        data = os.read(fd, 16)  # raw bytes, straight from the terminal
        # '\n' moves down to new line, and adding '\r' is for carriage return
        sys.stdout.write(repr(data) + "\r\n")
        sys.stdout.flush()

        if data in (b"q", b"\x03"):  # q or Ctrl-C
            break

finally:
    # restore the terminal settings to what they were before we set it to raw mode
    termios.tcsetattr(fd, termios.TCSAFLUSH, saved)
