from srcs.model.model import estimate_price, save_thetas
from srcs.training.data import load_dataset, normalize, denormalize


def gradient_step(
	coord: tuple[list[float], list[float]],
	thetas: tuple[float, float],
	learning_rate: float,
	lines: int
) -> tuple[float, float]:
	X = 0
	Y = 0
	sum_error = 0.0
	sum_error_x = 0.0

	index = 0
	while (index < len(coord[0]) and index < len(coord[1])):
		mileage = coord[X][index]
		price = coord[Y][index]

		error = estimate_price(mileage, thetas[0], thetas[1]) - price
		sum_error += error
		sum_error_x += error * mileage

		index += 1

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
	print("0%", end="", flush=True)
	for it in range(0, iterations):
		(theta0, theta1) = gradient_step(
			coord,
			(theta0, theta1),
			learning_rate,
			lines
		)
		
		print(f"\033[u\033[0K{round(((it - 1) / iterations) * 100)}%",
			end="",
			flush=True
		)
	print()
	return (theta0, theta1)


def main(dataset: str = "dataset/dataset.csv", learning_rate: float = 0.25, iterations: int = 2000) -> None:
	try:
		print("Loading dataset: ", end="\033[s")
		mileages, prices, lines = load_dataset(dataset)

		print("Training: ", end="\033[s")
		xs, lowest, highest = normalize(mileages)
		t0, t1 = train((xs, prices), learning_rate, iterations, lines)

		print()
		theta0, theta1 = denormalize(t0, t1, lowest, highest)
		save_thetas(theta0, theta1, "thetas.json")

		print("Result of training : ")
		print(f" - Theta0 : {theta0}")
		print(f" - Theta1 : {theta1}")
	except Exception as e:
		print(f"Error: {e}")


if (__name__ == "__main__"):
	main()
