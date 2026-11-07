import sys

from .bonus.plot import main as show_graph
from .model.model import load_thetas
from .prediction.predict import predict
from .render.render import render_screen, clear_lines
from .training.train import main as train_model
from .ui.keys import read_key


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


def run_action(name: str, dataset: str, params: tuple[float, int]) -> bool:
	if (name == "Train"):
		train_model(params[0], params[1], dataset)
	elif (name == "Predict"):
		predict()
	elif (name == "Show graph"):
		show_graph(dataset)
		clear_lines(20)
		return (True)
	return (False)


def wait_key() -> None:
	message = "\n\033[2mPress any key to go back to the menu...\033[0m"
	print(message, end="", flush=True)
	read_key()
	clear_lines(20)


def run_menu(dataset: str, thetas_path: str) -> None:
	options = ["Train", "Predict", "Show graph", "Exit"]
	selected, lines = 0, 0
	learning_rate = 0.1
	iterations = 5000
	message = ""

	try:
		while (True):
			thetas = get_thetas(thetas_path)
			trained = (thetas != (0.0, 0.0))
			if (lines > 0):
				clear_lines(lines)
			lines = render_screen(
				dataset, thetas, trained, options, selected, None, message
			)

			key = read_key()
			if (key in ("UP", "DOWN")):
				selected = move_selection(selected, key, len(options))
			elif (key == "EOF"):
				return
			elif (key == "ENTER"):
				message = ""
				name = options[selected]
				if (options[selected] == "Exit"):
					return
				if (not trained and name in ("Predict", "Show graph")):
					message = "Model not trained: run 'Train' first."
				else:
					lines = clear_lines(lines)
					print("\033[?25h", end="")
					skip_wait = False
					try:
						skip_wait = run_action(
							name, dataset, (learning_rate, iterations)
						)
					except KeyboardInterrupt:
						print("\nInterrupted")
					if (not skip_wait):
						wait_key()
	
	except KeyboardInterrupt:
		pass
	finally:
		print("\033[?25h")


def start_model() -> None:
	if (not sys.stdin.isatty()):
		print("Error: an interactive terminal is required")
		return
	run_menu("dataset.csv", "thetas.json")


if (__name__ == "__main__"):
	print("\033[?25l\033[H\033[2J", end="")
	start_model()
