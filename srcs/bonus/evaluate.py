import math

from srcs.model.model import estimate_price, load_thetas, split_dataset
from srcs.training.train import main as train_model
from srcs.training.data import load_dataset


def predict_all(
	mileages: list[float], theta0: float, theta1: float
) -> list[float]:
	return ([estimate_price(x, theta0, theta1) for x in mileages])


def mean_squared_error(
	prices: list[float], predictions: list[float]
) -> float:
	errors = [y - p for y, p in zip(prices, predictions, strict=True)]
	return (sum(e * e for e in errors) / len(errors))


def mean_absolute_error(
	prices: list[float], predictions: list[float]
) -> float:
	errors = [y - p for y, p in zip(prices, predictions, strict=True)]
	return (sum(abs(e) for e in errors) / len(errors))


def r_squared(prices: list[float], predictions: list[float]) -> float:
	mean_price = sum(prices) / len(prices)
	ss_res = sum(
		(y - p) ** 2 for y, p in zip(prices, predictions, strict=True)
	)
	ss_tot = sum((y - mean_price) ** 2 for y in prices)
	if (ss_tot == 0):
		raise ValueError("R2 is undefined: all prices are identical")
	return (1 - ss_res / ss_tot)


def main(dataset: str = "dataset.csv") -> None:
	try:
		print("Loading dataset: ", end="\033[s")
		mileages, prices, _ = load_dataset(dataset)
		(
			mileages,
			prices,
			test_mileages,
			test_prices
		) = split_dataset(mileages, prices, 0.80)

		theta0, theta1 = load_thetas("thetas.json")
		if (theta0 == 0.0):
			print("Warning model was not trained")
			print("Reload dataset for training: ", end="\033[s")
			train_model(dataset)
			theta0, theta1 = load_thetas("thetas.json")

		predictions = predict_all(mileages, theta0, theta1)
		mse = mean_squared_error(prices, predictions)

		print("\nEvalutions metrics:")
		print(f"MSE  : {mse:.2f}")
		print(f"RMSE : {math.sqrt(mse):.2f}")
		print(f"MAE  : {mean_absolute_error(prices, predictions):.2f}")
		print(f"R2   : {r_squared(prices, predictions):.4f}")
	except Exception as e:
		print(f"Error: {e}")


if (__name__ == "__main__"):
	main("dataset_large.csv")
