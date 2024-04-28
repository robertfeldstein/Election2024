# Statistical Analysis of 2024 Election Polling Data

The following GitHub repository was prepared by Robert Feldstein, working in conjunction with Professor Joe Guinness at Cornell University. 

The project is broken into a few working subdivisions:

1. Exploratory Data Analysis and Visualization (EDA)
2. Modules
3. Regression
4. Datasets
5. RFolder

## Exploratory Data Analysis and Visualization

This is a catch-all folder for investigating and visualizing interesting questions. At the time of producing this GitHub a lot of chatter has surrounded the role of RFK Junior in the upcoming election. It is unclear in regards to who he will "take" votes from between Joe Biden and Donald Trump. While we do not directly answer this question, we do look at how the spread between Joe Biden and Donald Trump has changed in response to changes in RFK's support. **As a matter of consistency, we define spread to be the difference between Donald Trump and Joe Biden in polling throughout the project.**

## Modules

A simple python program that uses selenium and pandas to scrape polling data from RealClearPolling. Please use this module responsibly!

## Regression

We tried several types of regression models to predict next-day polling results. In essence, poll prediction is a categorical regression problem. Our models work such that they predict the next day polling result for any possible poll that might be released. 

The models in this project include: Simple Linear Regression, Sinusoidal Regression, XGBoost Regression, and Gaussian Process Regression. 

## Datasets

Simple long-running prediction datasets created from running the regression models. These datasets were scored in R to determine which model performed the best. Overall, Gaussian Process Regression is able to defeat off the wall XGBoost regression. 

We hope this repository can serve as a jumping off point for other users seeking to perform statistical analysis on polling data. 

## RFolder 

Some regression models are best suited to be created in R, where categorical data is better handled. In particular, this package makes large use of R's GpGp package (created by Professor Guinness) to perform optimized Gaussian Process regression. 

In this repository we utilize code which scrapes data from RealClearPolitics. **We do not condone mass scraping of data from polling platforms.** Please utilize commands like time.sleep() to help limit strain on servers.

Thank you!

# Code Examples and Use Cases

Loading in the RealClearPolitics latest presidential polling data: 

```python
rcp = clean_data(get_poll_data())
```

Creating a simple sinusoidal regression dataframe: 

```python
scale = 365
days = df["Days Since 01-01-23"]
#Define some initial frequencies
frequencies = [i*2 for i in range(1, 10)]
def add_sine_cosine(df, freq, scale):
    df['sinfreq' + str(freq)] = np.sin(freq *np.pi*days/scale)
    df['cosfreq' + str(freq)] = np.cos(freq*np.pi*days/scale)
for freq in frequencies:
    add_sine_cosine(df, freq, scale)
frequency_strings = ['sinfreq' + str(freq) for freq in frequencies] + ['cosfreq' + str(freq) for freq in frequencies]
frequency_strings.append("Days Since 01-01-23")
#Display the data with new frequencies
df.head()
```

Building a Gaussian Process Model in R:
```R
library("GpGp")
y <- df$Trump..R. - df$Biden..D.
X <- model.matrix( ~ df$pollster )
locs <- df$Days.Since.01.01.23

m1 <- fit_model(y, locs, X, "matern_isotropic", silent = TRUE, m_seq = 50)
```

Diagrams: 


![rfk_pa](https://github.com/robertfeldstein/Election2024/assets/104737174/f24945bf-7042-4e57-8ad7-dfdc839c0963)

A simple regression diagram representing RFK's (a third party candidate's) polling performance in PA, a crucial battleground state in the upcoming presidential election. 




