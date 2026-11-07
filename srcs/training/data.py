def load_dataset(path: str) -> tuple[list[float], list[float], int]:
	with open(path, 'r') as datas:
		line = datas.readline().strip()
		if (not line or "km,price" not in line):
			raise TypeError(f"Incorect type for {path}")

		mileages = []
		prices = []
		lines = 0
		while (line):
			line = datas.readline().strip()
			if (line):
				mileages.append(float(line.split(',')[0]))
				prices.append(float(line.split(',')[1]))
				lines += 1
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
