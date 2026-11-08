import sys, time, math

from .model.model import save_thetas, load_thetas, split_dataset
from .render.render import render_screen, clear_lines
from .bonus.plot import compute_line_points, draw
from .training.data import normalize, denormalize
from .ui.settings import training_settings
from .prediction.predict import predict
from .training.train import train
from .bonus.evaluate import *
from .ui.keys import read_key
from .ui.utils import *


def show_graph(
	thetas_path: str, mileages: list[float], prices: list[float]
) -> None:
	try:
		theta0, theta1 = load_thetas(thetas_path)
		line_xs, line_ys = compute_line_points(
			theta0, theta1, min(mileages), max(mileages)
		)
		draw(mileages, prices, line_xs, line_ys)

	except Exception as e:
		print(f"\n\033[91mError: {e}\033[0m")
		wait_key()


def train_model(
	train_sett: tuple[float, int],
	thetas_path: str,
	mileages: list[float],
	prices: list[float]
) -> None:
	try:
		(
			mileages,
			prices,
			valid_mileages,
			valid_prices
		) = split_dataset(mileages, prices, 0.80)

		print("Training: ", end="\033[s")
		start = time.time()
		xs, lowest, highest = normalize(mileages)
		t0, t1 = train(
			(xs, prices), train_sett[0], train_sett[1], len(xs)
		)
		end = time.time()
		print()

		theta0, theta1 = denormalize(t0, t1, lowest, highest)
		save_thetas(theta0, theta1, thetas_path)

		print(f"Training duration: {round(end - start, 3)}s")
		print("Result of training : ")
		print(f" - Theta0 : {theta0}")
		if (theta1 > 0):
			print(f"\033[91m - Theta1 : {theta1}\033[0m")
			return
		print(f" - Theta1 : {theta1}\033[0m")
		print()

		predictions = predict_all(valid_mileages, theta0, theta1)
		mse = mean_squared_error(valid_prices, predictions)

		print("Precision Evaluation :")
		print(f"MSE  : {mse:.2f}")
		print(f"RMSE : {math.sqrt(mse):.2f}")
		print(f"MAE  : {mean_absolute_error(valid_prices, predictions):.2f}")
		print(f"R2   : {r_squared(valid_prices, predictions):.4f}")

	except Exception as e:
		print(f"\n\033[91mError: {e}\033[0m")


def run_action(
	name: str,
	thetas_path: str,
	train_sett: tuple[float, int],
	mileages: list[float],
	prices: list[float]
) -> int:
	if (name == "Train"):
		train_model(
			train_sett, thetas_path, mileages, prices
		)
	elif (name == "Predict"):
		predict()
	elif (name == "Show graph"):
		show_graph(thetas_path, mileages, prices)
		return (1)
	return (0)


def run_menu(dataset: str, thetas_path: str) -> None:
	options = ["Train", "Train settings", "Predict", "Show graph", "Exit"]
	mileages, prices = get_dataset_values(dataset)
	selected, lines = 0, 0
	train_sett = (0.1, 2000)
	message = ""

	try:
		print("\033[?25l\033[H\033[2J", end="")
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
					ret = 0
					try:
						if (name == "Train settings"):
							previous = dataset
							dataset, train_sett, ret = training_settings(
								dataset, train_sett
							)
							if (dataset != previous):
								save_thetas(0.0, 0.0, thetas_path)
								thetas = tuple((0.0, 0.0))
								mileages, prices = get_dataset_values(dataset)
								clear_lines(2)
						else:
							ret = run_action(
								name,
								thetas_path,
								train_sett,
								mileages,
								prices
							)
					except KeyboardInterrupt:
						print("\nInterrupted")
					if (ret == 0):
						wait_key()
					elif (ret == -1):
						break
	
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
