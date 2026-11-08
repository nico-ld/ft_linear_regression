import json
import os


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
	mileages: list[float], prices: list[float], test_part: float
) -> tuple[list[float], list[float], list[float], list[float]]:
	start_index = int(len(mileages) * test_part)
	test_mileages = []
	test_prices = []

	for index in range(start_index, len(mileages)):
		test_mileages.append(mileages[index])
		test_prices.append(prices[index])
	for index in range(len(mileages) - 1, start_index, -1):
		mileages.pop(index)
		prices.pop(index)
	return (mileages, prices, test_mileages, test_prices)
