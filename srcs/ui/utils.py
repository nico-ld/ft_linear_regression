from srcs.model.model import load_thetas
from srcs.render.render import clear_lines
from .keys import read_key


def get_thetas(path: str) -> tuple[float, float]:
	try:
		return (load_thetas(path))
	except (OSError, ValueError, KeyError):
		return (0.0, 0.0)


def move_selection(selected: int, key: str, count: int) -> int:
	if (key == "UP"):
		return ((selected - 1) % count)
	if (key == "DOWN"):
		return ((selected + 1) % count)
	return (selected)


def wait_key() -> None:
	message = "\n\033[2mPress any key to go back to the menu...\033[0m"
	print(message, end="", flush=True)
	read_key()
	clear_lines(20)
