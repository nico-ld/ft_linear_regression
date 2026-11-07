from srcs.model.model import load_thetas, estimate_price

def predict() -> None:
	try:
		theta0, theta1 = load_thetas("thetas.json")
		mileage = float(input("Enter your car's mileage: "))
		if (mileage < 0 or mileage != mileage):
			raise ValueError

		price = estimate_price(mileage, theta0, theta1)
		print(f"Estimate price: {round(price, 2)}$")
	except ValueError:
		print("Caught ValueError: Aborting")
	except Exception as e:
		print(f"Caught unexpected error: {e}")


if (__name__ == "__main__"):
	predict()
