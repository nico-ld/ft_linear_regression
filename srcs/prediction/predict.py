from srcs.model.model import load_thetas, estimate_price

def parse_float_input() -> float:
	ret = float(input("Enter your car's mileage : "))
	if (ret < 0 or ret != ret):
		raise ValueError
	return (ret)

def predict() -> None:
	try:
		theta0, theta1 = load_thetas("thetas.json")
		mileage = parse_float_input()

		price = estimate_price(mileage, theta0, theta1)
		print(f"Estimate price: {round(price, 2)}$")
	except ValueError:
		print("Caught ValueError: Aborting")
	except Exception as e:
		print(f"Caught unexpected error: {e}")


if (__name__ == "__main__"):
	predict()
