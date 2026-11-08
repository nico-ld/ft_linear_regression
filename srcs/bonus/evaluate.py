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


def get_color(
	objectives: list[float], value: float, smaller: bool = True
) -> str:
	colors = [
		"\033[92m", "\033[32m", "\033[93m", "\033[38;2;255;120;0m", "\033[91m"
	]

	for level in range(len(objectives)):
		if (smaller and value <= objectives[level]):
			return (colors[level])
		elif (not smaller and value >= objectives[level]):
			return (colors[level])
	return (colors[4])


def print_evaluation(
	predictions: list[float], test_prices: list[float]
) -> None:
	mean = sum(test_prices) / len(test_prices)
	rmse = math.sqrt(mean_squared_error(test_prices, predictions))
	mae = mean_absolute_error(test_prices, predictions)
	r2 = r_squared(test_prices, predictions) * 100

	rmse_percent = rmse / mean * 100
	mae_percent = mae / mean * 100
	rmse_style = get_color([7.0, 12.0, 18.0, 25.0], rmse_percent)
	mae_style = get_color([5.0, 10.0, 15.0, 22.0], mae_percent)
	r2_style = get_color([90.0, 80.0, 60.0, 30.0], r2, False)

	print("Precision Evaluation :")
	print(f"RMSE (objective < 7%) : {rmse_style}{rmse_percent:.2f}%\033[0m")
	print(f"MAE (objective < 5%)  : {mae_style}{mae_percent:.2f}%\033[0m")
	print(f"R2 (objective > 90%)  : {r2_style}{r2:.2f}%\033[0m")


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

		predictions = predict_all(test_mileages, theta0, theta1)
		print_evaluation(predictions, test_prices)

	except Exception as e:
		print(f"Error: {e}")


if (__name__ == "__main__"):
	main()
