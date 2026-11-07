def render_line(text: str, style: str = "", width: int = 50) -> None:
	padded = text[:width].ljust(width)
	print(f"│{style}{padded}\033[0m│")


def render_header(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	width: int = 50
) -> None:
	border = "─"
	print(f"┌{border * width}┐")
	render_line(f" dataset: {dataset}", "", width)
	render_line(f" theta0: {thetas[0]}", "", width)
	render_line(f" theta1: {thetas[1]}", "", width)
	if (trained):
		render_line(" model: trained", "\033[32m", width)
	else:
		render_line(" model: needs training", "\033[31m", width)


def render_separator(width: int = 50) -> None:
	border = "─"
	print(f"├{border * width}┤")


def render_menu(options: list[str], selected: int, width: int = 50) -> None:
	for index, label in enumerate(options):
		style = "\033[7m" if (index == selected) else ""
		render_line(f" {label}", style, width)


def render_footer(width: int = 50) -> None:
	border = "─"
	print(f"└{border * width}┘")



def render_screen(
	dataset: str,
	thetas: tuple[float, float],
	trained: bool,
	options: list[str],
	selected: int
) -> None:
	print("\033[?25l\033[H\033[2J", end="")
	print("\033[1mft_linear_regression\033[0m")
	render_header(dataset, thetas, trained)
	render_separator()
	render_menu(options, selected)
	render_footer()
	print("\033[2m ↑/↓ move   Enter select\033[0m")
