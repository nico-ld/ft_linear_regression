import matplotlib.pyplot as plt

from srcs.model.model import estimate_price, load_thetas
from srcs.training.data import load_dataset


def compute_line_points(
	theta0: float, theta1: float, lowest: float, highest: float
) -> tuple[list[float], list[float]]:
	xs = [lowest, highest]
	ys = [estimate_price(x, theta0, theta1) for x in xs]
	return (xs, ys)


def draw(
	mileages: list[float],
	prices: list[float],
	line_xs: list[float],
	line_ys: list[float],
) -> None:
	fig, ax = plt.subplots()
	ax.scatter(mileages, prices, label="data")
	ax.plot(line_xs, line_ys, color="red", label="regression line")
	ax.set_xlabel("mileage (km)")
	ax.set_ylabel("price")
	ax.set_title("Car price by mileage")
	ax.legend()
	plt.show()


def main(dataset: str = "dataset.csv") -> None:
	try:
		print("Loading dataset: ", end="\033[s")
		mileages, prices, _ = load_dataset(dataset)

		theta0, theta1 = load_thetas("thetas.json")
		line_xs, line_ys = compute_line_points(
			theta0, theta1, min(mileages), max(mileages)
		)
		draw(mileages, prices, line_xs, line_ys)
	except Exception as e:
		print(f"Error: {e}")


if (__name__ == "__main__"):
	main()
