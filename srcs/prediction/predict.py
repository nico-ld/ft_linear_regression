from srcs.model.model import load_thetas, estimate_price
from srcs.training.train import main as train_model


def parse_float_input(message: str) -> float:
	ret = float(input(message))
	if (ret < 0 or ret != ret):
		raise ValueError
	return (ret)

def predict(dataset: str = "dataset.csv") -> None:
	try:
		theta0, theta1 = load_thetas("thetas.json")
		if (theta0 == 0.0):
			print("Warning model was not trained")
			print("Reload dataset for training: ", end="\033[s")
			train_model(dataset)
			theta0, theta1 = load_thetas("thetas.json")

		mileage = parse_float_input("Enter your car's mileage : ")
		price = estimate_price(mileage, theta0, theta1)
		print(f"Estimate price: {round(price, 2)}$")
	except ValueError:
		print("\033[91mCaught ValueError: Aborting\033[0m")
	except Exception as e:
		print(f"\033[91mCaught unexpected error: {e}\033[0m")


if (__name__ == "__main__"):
	predict()
