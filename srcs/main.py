from .training.data import load_dataset
from .render.render import render_header, render_footer


def home(dataset: str, thetas: tuple[float, float]) -> None:
	render_header(dataset, thetas)
	render_footer()


def start_model() -> None:
	dataset = "dataset.csv"
	theta0 = 8720.060741622161
	theta1 = -0.026374946431909636
	home(dataset, (theta0, theta1))


# ┌┐─│└┘
if (__name__ == "__main__"):
	print("\033[2J\033[1mft_linear_regression\033[0m")
	start_model()
