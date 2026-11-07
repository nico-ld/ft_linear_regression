import sys

from bonus.plot import main as show_graph
from model.model import load_thetas
from prediction.predict import predict
from render.render import render_screen
from training.train import main as train_model
from ui.keys import read_key


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


def run_action(name: str, dataset: str, trained: bool) -> None:
	learning_rate = 0.1
	iterations = 5000

	if (name == "Train"):
		train_model(learning_rate, iterations, dataset)
	elif (not trained):
		print("\033[91mModel not trained: rn 'Train' first.\033[0m")
	elif (name == "Predict"):
		predict()
	elif (name == "Show graph"):
		show_graph(dataset)


def wait_key() -> None:
	message = "\n\033[2mPress any key to go back to the menu...\033[0m"
	print(message, end="", flush=True)
	read_key()


def run_menu(dataset: str, thetas_path: str) -> None:
	options = ["Train", "Predict", "Show graph", "Exit"]
	selected = 0

	try:
		while (True):
			thetas = get_thetas(thetas_path)
			trained = (thetas != (0.0, 0.0))
			render_screen(dataset, thetas, trained, options, selected)

			key = read_key()
			if (key in ("UP", "DOWN")):
				select = move_selection(selected, key, len(options))
			elif (key == "EOF"):
				return
			elif (key == "ENTER"):
				if (options[selected] == "Exit"):
					return
				print("\033[?25h\033[H\033[2J", end="")
				try:
					run_action(options[selected], dataset, trained)
				except KeyboardInterrupt:
					print("\nInterrupted")
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
	start_model()
