# Statistical Analysis of 2024 Election Polling Data

The following GitHub repository was prepared by Robert Feldstein, working in conjunction with Professor Joe Guinness at Cornell University. 

The project is broken into a few working subdivisions:

1. Exploratory Data Analysis and Visualization (EDA)
2. Modules
3. Regression
4. Datasets
5. RFolder

## Exploratory Data Analysis and Visualization

This is a catch-all folder for investigating and visualizing interesting questions. At the time of producing this GitHub a lot of chatter has surrounded the role of RFK Junior in the upcoming election. It is unclear in regards to who he will "take" votes from between Joe Biden and Donald Trump. While we do not directly answer this question, we do look at how the spread between Joe Biden and Donald Trump has changed in response to changes in RFK's support. **As a matter of consistency, we define spread as Donald Trump's polling numbers minus Joe Biden's.**

## Modules

A simple python program that uses selenium and pandas to scrape polling data from RealClearPolling. Please use this module responsibly!

## Regression

We tried several types of regression models to predict next-day polling results. In essence, poll prediction is a categorical regression problem. Our models work such that they predict the next day polling result for any possible poll that might be released. 

The models in this project include: Simple Linear Regression, Sinusoidal Regression, XGBoost Regression, and Gaussian Process Regression. 

## Datasets

Simple long-running prediction datasets created from running the regression models. These datasets were scored in R to determine which model performed the best. Overall, Gaussian Process Regression is able to defeat off the shelf XGBoost regression. 

We hope this repository can serve as a jumping off point for other users seeking to perform statistical analysis on polling data. 

## RFolder 

Some regression models are best suited to be created in R, where categorical data is better handled. In particular, this package makes large use of R's GpGp package (created by Professor Guinness) to perform optimized Gaussian Process regression. 

In this repository we utilize code which scrapes data from RealClearPolitics. **We do not condone mass scraping of data from polling platforms.** Please utilize commands like time.sleep() to help limit strain on servers.

Thank you!

# Code Examples and Use Cases

Using Python to load in datasets: 
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


Sample Analyses:


As part of this project, we looked at how individual candidates were performing across core battleground states such as PA, MI, WI, FL, GA, and AZ. Using a locally weighted regression, we were able to characterize several candidate trends in key states. The following plot shows RFK's performance in PA since May of 2023. Note that the first polling point is an outlier, and most likely indicates % of voters who would vote for RFK in a head to head with Biden or a head to head with Trump. Later polling shows that RFK's sizable support has cut roughly in half. Still 10% of the vote in a battleground state like PA could fundamentally alter the entire race. 

![rfk_pa](https://github.com/robertfeldstein/Election2024/assets/104737174/f24945bf-7042-4e57-8ad7-dfdc839c0963)


We were interested in what effect RFK's presence in the race would have on the other two candidates's polling numbers. To investigate this, we looked at polls that asked respondents who they preferred between Trump and Biden, and who they preferred when more options were given, such as RFK Jr., Jill Stein, and Cornell West. In the figure below, we see that there exists a slight positive trend between RFK's polling average and Trump's polling. Despite this, we find that RFK's effect on the election is inconclusive at this point. Due to the relative infrequent release of polls and RFK's flat polling average, we do not have enough evidence yet to claim RFK pulls voters more from one candidate than another. 

![rkf_spread](https://github.com/robertfeldstein/Election2024/assets/104737174/aa7506f5-155e-4d9b-baa8-19e0979f7bf7)

A large portion of our analysis was spent on treating the type of polling company as a categorical variable. In particular, it was interesting to study how the overall spread in polling between Joe Biden and Donald Trump could vary widely over the same across pollsters. In practice, we found that Gaussian Process regression performed remarkably similar to the discretized polls released by companies. The following figure shows a simple gaussian process regression representing the observed difference in national polling between Donald Trump and Joe Biden, as reported by CNBC.

![polling_spread_regression](https://github.com/robertfeldstein/Election2024/assets/104737174/292dc93f-83c8-46fc-adb6-700b84625d1e)


