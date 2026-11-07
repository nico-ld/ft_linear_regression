import os

from srcs.render.render import render_screen, clear_lines
from srcs.ui.utils import move_selection, wait_key
from .keys import read_key


def check_dataset(path: str) -> None:
	if (not os.path.isfile(path)):
		raise ValueError(f"{path}: file not found")
	with open(path, "r") as file:
		lines = file.readline()
	if (not lines or "km,price" not in lines[0]):
		raise ValueError(f"{path}: header 'km,price' expected")
	if (len(lines) < 3):
		raise ValueError(f"{path}: at least 2 data rows are needed")


def ask_dataset(current: str) -> str:
	new = input("Enter the new path for dataset : ").strip()
	if (not new or new == current):
		print("Dataset unchanged.")
		return (current)
	check_dataset(new)
	print("Dataset updated, the model has to trin on the new values.")
	return (new)


def ask_learning_rate(current: float) -> float:
	message = "Enter the new Learning Rate (0 < value <= 1) : "
	text = input(message).strip()
	if (not text):
		return (current)
	value = float(text)
	if (not 0 < value <= 1):
		raise ValueError("it must be in ]0, 1]")
	return (value)


def ask_iterations(current: int) -> int:
	maximum = 1000000
	message = f"Enter the new amount of Iterations (1 - {maximum}) : "
	text = input(message).strip()
	if (not text):
		return (current)
	value = int(text)
	if (not 1 <= value <= maximum):
		raise ValueError(f"it must be between 1 and {maximum}")
	return (value)


def update_value(
	dataset: str, train_sett: tuple[float, int], name: str
) -> tuple[str, tuple[float, int]]:
	learning_rate, iterations = train_sett

	if (name == "Dataset"):
		dataset = ask_dataset(dataset)
	elif (name == "Learning Rate"):
		learning_rate = ask_learning_rate(learning_rate)
	elif (name == "Iterations"):
		iterations = ask_iterations(iterations)
	return (dataset, (learning_rate, iterations))


def training_settings(
	dataset: str, train_sett: tuple[float, int]
) -> tuple[str, tuple[float, int], int]:
	options = ["Dataset", "Learning Rate", "Iterations", "Go back"]
	selected, lines = 0, 0
	ret = 1

	try:
		while (True):
			if (lines > 0):
				clear_lines(lines)
			lines = render_screen(
				dataset, (0.0, 0.0), False, options, selected, train_sett
			)

			key = read_key()
			if (key in ("UP", "DOWN")):
				selected = move_selection(selected, key, len(options))
			elif (key == "EOF"):
				ret = -1
				break
			elif (key == "ENTER"):
				name = options[selected]

				if (options[selected] == "Go back"):
					break
				lines = clear_lines(lines)
				print("\033[?25h", end="")
				try:
					dataset = train_sett = update_value(
						dataset, train_sett, name
					)
				except KeyboardInterrupt:
					print("\nInterrupted")
				except ValueError as error:
					print(f"\n\033[91m{name} unchanged: {error}\033[0m")
				wait_key()

	except KeyboardInterrupt:
		ret = -1
	finally:
		print("\033[?25h")
	if (ret >= 0):
		clear_lines(lines)
	return (dataset, train_sett, ret)

