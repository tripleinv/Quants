# Quantitative Strategies Projects Repository
This repository contains two key projects focusing on factor-based investment strategies. The first project focuses on a value-based factor portfolio strategy using the Price-to-Book (P/B) ratio, while the second project targets a growth-based factor portfolio strategy concentrating on earnings surprises.

1. Value-Based Factor Portfolio Strategy (P/B Ratio)
Overview
The value-based strategy project aims to construct portfolios by ranking stocks based on their P/B ratios. Lower P/B ratios are assumed to indicate undervalued stocks, which are targeted for the "high value" portfolio. The project involves data acquisition, cleaning, analysis, and backtesting to assess the performance of the strategy over several years.

**Steps:** (all detailed code/steps/outputs can be found in notebook P1-P5)
Data Preparation and Manipulation: 
- Work with the SEC database through SEC API.
- Added historically removed tickers to eliminiate survivorship bias. 
Analysis:
- Calculate and analyze monthly return data.
- Rank stocks based on P/B values and assign to top and bottom portfolios.
- Calculate cumulative returns and compare against the S&P 500 benchmark.
Performance Evaluation:
- Assess performance using metrics such as Sharpe Ratio, Drawdown, and others.
- Conduct sector concentration analysis to understand risk exposure.

**Results & Insights**
The insights from this project indicate that value-based factors, specifically low P/B strategy, have underperformed the high P/B strategy over the past few years. In particular, during the 2020 pandemic lockdown, low P/B strategy has significantly underperformned. In other words, during the economic downturn, investors would prefer high quality stocks, which would normally trade at a slight premium to low quality in terms of price/book value. Nevertheless, over the past decade, both high and low P/B factor investment strategy have outrun the S&P500 index benchmark. When looking at risk to reward profile, long high P/B represented the highest returns with a modest risks compared to long low P/B factor. Sector-wise, historically, financial represented the largest group among the low P/B factor, followed by energy.

Insights and recommendations are provided on the following key areas:


![cumulative_returns_of_low_and_high_PBVPS_strategy](https://github.com/user-attachments/assets/8a2fe9b0-7fef-410a-b69c-de21c7dc9072)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![relative_performance_of_low_pb_high_pb](https://github.com/user-attachments/assets/a4618e12-2ffc-4965-a8b6-c5ddbe12be83)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![low pb value risk reward characteristics](https://github.com/user-attachments/assets/2789247b-b5fa-446c-8e11-4ee9862f50a0)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![low_pb_value_sector_concentration](https://github.com/user-attachments/assets/57ab82fd-6599-42f8-8288-8a335e19ad6e)


2. Growth-Based Factor Portfolio Strategy (Earnings Surprise)
Overview
This project leverages earnings surprise data to create a dynamic portfolio that aims to capitalize on the market's reaction to earnings reports. The strategy is based on the research conducted on PEAD (Post Earnings Announcement Drift), which stated the tendency for a stock’s cumulative abnormal returns to drift in the direction of an earnings surprise for several weeks (even several months) following an earnings announcement. 

**Steps:**(all detailed code/steps/outputs can be found in notebook P6)
Data Sourcing: Download and merge datasets from Compustat, CRSP, and I/B/E/S.
Strategy Design:
- Filter for the most recent quarterly earnings estimates and actuals before the announcement date.
- Calculate the decay factor of earnings surprises to weight the influence of older surprises less.
- Construct monthly earnings surprise factors and rebalance portfolios accordingly on a monthly basis.
Backtesting:
- Analyze the cumulative returns for portfolios constructed from the top 20% and bottom 20% of stocks based on earnings surprises.
- Draw comparisons with the S&P 500 to gauge relative performance.
- Assess performance using metrics such as Sharpe Ratio, Drawdown, and others.
- Conduct sector concentration analysis to understand risk exposure.
**Results & Insights**
The growth-based strategy, focused on earnings surprises, shows significant potential in capturing excess returns post-earnings announcements with positive earnings surprise. Over the past decade, long positive earnings surprise has outperformed the negative earnings surprise and the S&P500 indexes. While it comes with higher volatility, the returns is also correspondingly higher. When looking at the Sharpe Ratio, long positive earnings surprise factor has delivered a rate of 56%, compared to the 48% by negative earnings surprise. However, it also underscores the importance of timing and fast execution due to the quickly diminishing effects of surprises.


![cumulative returns of positive and negative earnings surprise](https://github.com/user-attachments/assets/e2def168-c8dd-4011-b639-0c7ec01e9585)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![relative performance of negative and positive earnings surprise](https://github.com/user-attachments/assets/741e6665-1d69-4fd3-9f20-71afaab0303a)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![long positive and negative earnings surprise value risk reward](https://github.com/user-attachments/assets/47c4df31-141b-480e-b6b3-ced473d86ea1)
**--------------------------------------------------------------------------------------------------------------------------------------------------**
![positive earnings surprise factor sector concentration](https://github.com/user-attachments/assets/13f14548-9be4-4614-aaf6-c1e88a56750d)



# Assumptions and Caveats:

Throughout the analysis, multiple assumptions were made to manage challenges with the data. These assumptions and caveats are noted below:

* Assumption 1 (ex: in the value-based factor project, when working with the SEC database, the integrity of the dataset is limited, so the calculation for the company's book value is based on varioius matrics depends on their availability. More details are discussed in P1 and P4)
  
* Assumption 2 (ex: in the growth-based factor project, factor decay is calcualted as (number of days passed announcement * -1.5%), assuming that normally the impact of surprise would last 60 days according to Bernard, V. L., & Thomas, J. K. (1990). Evidence that stock prices do not fully reflect the implications of current earnings for future earnings. Journal of Accounting and Economics, 13(4), 305-340
