from srcs.render.render import render_screen, clear_lines
from srcs.main import move_selection, wait_key, get_thetas
from srcs.prediction.predict import parse_float_input
from .keys import read_key

def update_value(
	dataset: str,
	train_sett: tuple[float, int],
	thetas: tuple[float, float],
	name: str
) -> None:
	if (name == "Dataset"):
		dataset = input("Enter the new path for dataset : ")
		thetas[0], thetas[1] = get_thetas(dataset)
	elif (name == "Learning Rate"):
		train_sett[0] = parse_float_input("Enter the new Learning Rate : ")
	elif (name == "Iterations"):
		message = "Enter the new amount of Iterations : "
		train_sett[1] = int(parse_float_input(message))


def training_settings(
		dataset: str, train_sett: tuple[float, int]
) -> int:
	options = ["Dataset", "Learning Rate", "Iterations", "Go back"]
	selected, lines = 0, 0
	ret = 0

	try:
		while (True):
			if (lines > 0):
				clear_lines(lines)
			lines = render_screen (
				dataset, None, False, options, selected, train_sett
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
				print("\033[?25h", end = "")
				try:
					update_value(dataset, train_sett[0], train_sett[1], name)
				except KeyboardInterrupt:
					print("\nInterrupted")
				except ValueError:
					print(f"\nCaught a ValueError for {name}")
				wait_key()

	except KeyboardInterrupt:
		ret = -1
	finally:
		print("\033[?25h")
	return (ret)

