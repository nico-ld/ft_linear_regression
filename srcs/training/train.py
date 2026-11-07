from srcs.model.model import estimate_price, save_thetas
from srcs.training.data import load_dataset, normalize, denormalize
import sys


def gradient_step(
	coord: tuple[list[float], list[float]],
	thetas: tuple[float, float],
	learning_rate: float,
	lines: int
) -> tuple[float, float]:
	sum_error = 0.0
	sum_error_x = 0.0

	index = 0
	while (index < len(coord[0]) and index < len(coord[1])):
		x = coord[0][index]
		y = coord[1][index]

		error = estimate_price(x, thetas[0], thetas[1]) - y
		sum_error += error
		sum_error_x += error * x

	new_theta0 = thetas[0] - learning_rate * sum_error / lines
	new_theta1 = thetas[1] - learning_rate * sum_error_x / lines
	return (new_theta0, new_theta1)


def train(
	coord: tuple[list[float], list[float]],
	learning_rate: float,
	iterations: int,
	lines: int
) -> tuple[float, float]:
	theta0, theta1 = 0.0, 0.0
	for it in range(0, iterations):
		(theta0, theta1) = gradient_step(
			coord,
			(theta0, theta1),
			learning_rate,
			lines
		)
	return (theta0, theta1)


def main(learning_rate: float = 0.1, iterations: int = 1000) -> None:
	try:
		learning_rate = 0.1
		iterations = 1000
		mileages, prices, lines = load_dataset("data.csv")
		xs, lowest, highest = normalize(mileages)
		t0, t1 = train((xs, prices), learning_rate, iterations, lines)
		theta0, theta1 = denormalize(t0, t1, lowest, highest)
		save_thetas(theta0, theta1, "thetas.json")
	except Exception as e:
		print(f"Caught an Unexepected error: {e}")


if (__name__ == "__main__"):
	main(float(sys.argv[1]), int(sys.argv[2]))
