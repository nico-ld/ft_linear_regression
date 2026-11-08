import json, os, random


def estimate_price(mileage: float, theta0: float, theta1: float) -> float:
	return (theta0 + theta1 * mileage)


def save_thetas(theta0: float, theta1: float, path: str) -> None:
	with open(path, 'w') as file:
		json.dump({"theta0": theta0, "theta1": theta1}, file)


def load_thetas(path: str) -> tuple[float, float]:
	if (not os.path.exists(path)):
		return (0.0, 0.0)

	with open(path, 'r') as thetas:
		thetas_dict = json.load(thetas)
	return (thetas_dict["theta0"], thetas_dict["theta1"])


def split_dataset(
	mileages: list[float],
	prices: list[float],
	train_part: float,
	seed: int = 7
) -> tuple[list[float], list[float], list[float], list[float]]:
	indexes = list(range(len(mileages)))
	random.Random(seed).shuffle(indexes)

	cut = int(len(indexes) * train_part)
	train = indexes[:cut]
	test = indexes[cut:]
	return (
		[mileages[i] for i in train],
		[prices[i] for i in train],
		[mileages[i] for i in test],
		[prices[i] for i in test],
	)
