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
	@rm -rf srcs/__pycache__
	@rm -rf srcs/bonus/__pycache__
	@rm -rf srcs/model/__pycache__
	@rm -rf srcs/prediction/__pycache__
	@rm -rf srcs/render/__pycache__
	@rm -rf srcs/training/__pycache__
	@rm -rf srcs/ui/__pycache__
	@rm -f thetas.json
