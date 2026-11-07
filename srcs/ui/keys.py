import os, sys, termios, tty


def read_key() -> str:
	fd = sys.stdin.fileno()
	saved = termios.tcgetattr(fd)
	try:
		tty.setcbreak(fd, termios.TCSANOW)
		data = os.read(fd, 3)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, saved)

	if (data in (b"\x1b[A", b"\x1bOA")):
		return ("UP")
	if (data in (b"\x1b[B", b"\x1bOB")):
		return ("DOWN")
	if (data in (b"\n", b"\r")):
		return ("ENTER")
	if (data in (b"", b"\x04")):
		return ("EOF")
	return ("OTHER")
