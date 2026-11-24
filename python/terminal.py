import termios, tty


class RawTerminal:
    def __init__(self, file_descriptor: int):
        self._file_descriptor = file_descriptor

    def __enter__(self):
        self._saved = termios.tcgetattr(self._file_descriptor)
        tty.setraw(self._file_descriptor)
        # write(CSI + '?1049h' + CSI + '?2004h')
        return self

    def __exit__(self, exc_type, exc, tb):
        # write(CSI + '?2004l' + CSI + '?1049l' + CSI + '0m' + CSI + '?25h')
        termios.tcsetattr(self._file_descriptor, termios.TCSAFLUSH, self._saved)
