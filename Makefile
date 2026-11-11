all:
	@python3 -m srcs.main

train:
	@python3 -m srcs.training.train

predict:
	@python3 -m srcs.prediction.predict

evaluate:
	@python3 -m srcs.bonus.evaluate

plot:
	@python3 -m srcs.bonus.plot

clean:
	@printf "Cleaning workspace..\033[2m\n"
	@find -type d -name "__pycache__" -prune -printf "\tRemoving: " -print -exec rm -rf -- {} +
	@printf "\033[0mWorkspace cleaned !\n"
	@rm -f thetas.json
