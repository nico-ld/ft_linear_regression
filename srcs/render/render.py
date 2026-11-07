def render_line(text: str, style: str = "", width: int = 50) -> int:
	padded = text[:width].ljust(width)
	print(f"│{style}{padded}\033[0m│")
	return (1)


def render_header(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	width: int = 50
) -> int:
	border = "─"
	count = 1

	print(f"┌{border * width}┐")
	count += render_line(f" dataset: {dataset}", "", width)
	count += render_line(f" theta0: {thetas[0]}", "", width)
	count += render_line(f" theta1: {thetas[1]}", "", width)
	if (trained):
		count += render_line(" model: trained", "\033[32m", width)
	else:
		count += render_line(" model: needs training", "\033[31m", width)
	return (count)


def render_separator(width: int = 50) -> int:
	border = "─"
	print(f"├{border * width}┤")
	return (1)


def render_menu(options: list[str], selected: int, trained: bool, width: int = 50) -> int:
	count = 0
	for index, label in enumerate(options):
		style = ""
		if ((index == 1 or index == 2) and not trained):
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
	message_error: str = ""
) -> int:
	print("\033[?25l", end="")
	print("\033[1mft_linear_regression\033[0m")
	count = 1
	count += render_header(dataset, thetas, trained)
	count += render_separator()
	count += render_menu(options, selected, trained)
	count += render_footer()
	if (message_error):
		print(f"\033[91m {message_error}\033[0m")
		count += 1
	print(f"\033[2m ↑/↓ move   Enter select | [DEBUG] : lines printed: {count + 1}\033[0m")
	return (count + 1)
