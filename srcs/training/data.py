def load_dataset(path: str) -> tuple[list[float], list[float], int]:
	with open(path, 'r') as file:
		datas = file.readlines()
		lines = len(datas) - 1
		if (lines <= 0):
			print("\033[91mError\033[0m")
			raise ValueError(f"Empty dataset")
		elif ("km,price" not in datas[0].strip()):
			print("\033[91mError\033[0m")
			raise TypeError(f"Incorect header for {path}")

		mileages = []
		prices = []
		index = 1
		print("0%", end="", flush=True)

		while (index <= lines):
			mileages.append(float(datas[index].split(',')[0]))
			prices.append(float(datas[index].split(',')[1]))
			index += 1
			print(f"\033[u\033[0K{round(((index - 1) / lines) * 100)}%", end="", flush=True)
	print()
	return (mileages, prices, lines)


def normalize(values: list[float]) -> tuple[list[float], float, float]:
	lowest = min(values)
	highest = max(values)
	if (lowest == highest):
		raise ZeroDivisionError
	return ([(v - lowest) / (highest - lowest) for v in values], lowest, highest)


def denormalize(
	t0: float, t1: float,
	lowest: float, highest: float
) -> tuple[float, float]:
	value_range = highest - lowest
	theta1 = t1 / value_range
	theta0 = t0 - t1 * lowest / value_range
	return (theta0, theta1)
