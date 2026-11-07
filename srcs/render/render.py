def render_line(text: str, style: str = "", width: int = 50) -> int:
	padded = text[:width].ljust(width)
	print(f"│{style}{padded}\033[0m│")
	return (1)


def header_content(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	train_sett: tuple[float, int],
	width: int = 50
) -> int:
	count = 0
	count += render_line(f" dataset: {dataset}", "", width)
	
	if (train_sett is not None):
		count += render_line(f" Learning Rate: {train_sett[0]}", "", width)
		count += render_line(f" Iterations: {train_sett[1]}", "", width)

	else:
		count += render_line(f" theta0: {thetas[0]}", "", width)
		count += render_line(f" theta1: {thetas[1]}", "", width)
		if (trained):
			count += render_line(" model: trained", "\033[32m", width)
		else:
			count += render_line(" model: needs training", "\033[31m", width)
	return (count)



def render_header(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	train_sett: tuple[float, int],
	width: int = 50
) -> int:
	border = "─"
	count = 1
	print(f"┌{border * width}┐")
	count += header_content(dataset, thetas, trained, train_sett)
	return (count)


def render_separator(width: int = 50) -> int:
	border = "─"
	print(f"├{border * width}┤")
	return (1)


def render_menu(options: list[str], selected: int, trained: bool, width: int = 50) -> int:
	count = 0
	for index, label in enumerate(options):
		style = ""
		if (not trained and label in ("Predict", "Show graph")):
			style += "\033[2m"
		if (index == selected):
			style += "\033[7m"
		count += render_line(f" {label}", style, width)
	return (count)


def render_footer(width: int = 50) -> int:
	border = "─"
	print(f"└{border * width}┘")
	return (1)


def clear_lines(count: int) -> int:
	line = 1

	print("\033[1;1H", end="", flush=True)
	while (line <= count):
		print("\033[0K\033[1B", end="", flush=True)
		line += 1
	print("\033[1;1H", end="", flush=True)
	return (0)
	

def render_screen(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	options: list[str],
	selected: int,
	train_sett: tuple[float, int] = None,
	message_error: str = ""
) -> int:
	print("\033[?25l", end="")
	print("\033[1mft_linear_regression\033[0m")
	count = 2
	count += render_header(dataset, thetas, trained, train_sett)
	count += render_separator()
	count += render_menu(options, selected, trained)
	count += render_footer()
	if (message_error):
		print(f"\033[91m {message_error}\033[0m")
		count += 1
	print("\033[2m ↑/↓ move   Enter select \033[0m")
	return (count)
