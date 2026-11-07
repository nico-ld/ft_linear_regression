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
	return (thetas_dict["thetas0"], thetas_dict["thetas1"])
