# ft_linear_regression

## Description

**ft_linear_regression** is the first step in AI and Machine Learning. The objective is to create a linear regression algorithm that predict the price of a car, depending on its mileage.

## Usage

Cause I learn it, I implement a Makefile in this Python project. With it you can : 
- **Train the model**, by default the model is train with dataset.csv, but you can change it in code. Other function will train the model automatically if it wasn't trained before, because this function save the 2 thetas that represent model parameters.

```bash
make train
```

- **Predict a price**, execute this command then enter a mileage, the model will return you the appropriate price

```bash
make predict
```


- **Visualize result on a graph**, this command will show you a representation of the regression line between every datas

```bash
make plot
```

- **Evaluate the model**, This command will train again the model, but it splits the dataset to keep a part aside and evaluate the model on it. So even if the model was trained, thetas will be overwrited by this call

```bash
make evaluate
```
