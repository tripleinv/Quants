# Event Study Project (P7): Trump's Presidency Impact on Stock's Abnormal Returns
## Background
"What does it mean for the stock market if Donald Trump is re-elected as the President of the United States?" This is a hot topic that's buzzling around the world currently. This year, it's a nail-biter with the VP Kamala Harris and former President Donald Trump going head-to-head, both vying for the top spot.
To better predict what's going to happen if Trump wins, it's essential to understand the history, that is, what happened in 2016? Was there an opportunity to generate alpha driven by the election result? Or did the market already price in the much anticipated Trump's policies, including de-regulation, tax cuts and renegotiating trade policies on industries like Banking, Energy and Construction? 
To uncover the hidden story, this project is focused on discovering the man behind the curtain.

**Insights and recommendations are provided on the following key areas:**
- **Factor Models Comparison Between Fama-French and Market**: Estimated expected returns based on parameters obtained during the estimation period for both Fama-French model and Market Model using Ordinary least squares('OLS') method. 
- **Sector Returns and Volatiltiy Statistics Comparison**: Calculated and Compared various sector returns, such as cumulative returns, abnormal returns, standardized abnormal returns and their corresponding volatitlies and t-statistics.  
- **Factor Exposures For Various Sectors**: Discussed factor exposures for Financial, Energy and Technology sectors and explained the sector's performance based on its corresponding models. 
- **Event Windows Analysis**: Breakdown of various returns during the event windown and analyzed different return outcomes using different event window.
  
### Strategy Design Methodology:
- Event Study Timeline: in this study, two set of timeline parameters are applied for the research: the first timeset is (estwin=100, gap=50, evtwins=-10, evtwine=10), the second timeset is (estwin=100, gap=50, evtwins=-20, evtwine=20). estwin is the length of estimation period in trading days, start and end define the event window around the event date (day 0), gap is the space between the estimation period and event window to prevent information leakage. The timeline is as followed: ![event_study_timeline](https://github.com/user-attachments/assets/255dec7c-7cd8-4c49-a876-206dd4c136f3)
- Two risk model estimation is applied, including Fama-French and Market models. The results of alphas and betas are calculated from performing the OLS regression. 
- Various returns metrics are used to compare the results: Abnormal Returns (AR), Buy-and-Hold Abnormal Returns (BHAR), Standardized Abnormal Returns (SAR) and their corresponding cumulative returns.
- T-statistics are calculated to gauge the statistic significance of the result. 
  
### Techniques used in this Event Study project:
Data Collection and Preparation:
- Utilized complex SQL queries to extract stock return data and factor returns from CRSP and Fama-French databases.
- Employed pandas for data manipulation, merging stock data with factor returns, and handling date alignments.

Event Study Methodology:
- Implemented both Market Model and Fama-French Three-Factor Model for estimating expected returns.
- Calculated abnormal returns (AR), cumulative abnormal returns (CAR), and buy-and-hold abnormal returns (BHAR) using vectorized operations in pandas.
- Applied rolling window calculations for estimation periods and event windows.

Statistical Analysis:
- Computed t-statistics and p-values for assessing the statistical significance of abnormal returns.
- Utilized OLS regression from statsmodels for factor model estimation.

Sector Analysis:
- Grouped stocks by sector to analyze differential impacts across industries.
- Calculated sector-specific betas and factor loadings.

Data Visualization:

Used matplotlib and seaborn for creating time series plots of cumulative abnormal returns.
Developed heatmaps to visualize cross-sectional abnormal returns across different event window days.

Performance Optimization:

Leveraged pandas' vectorized operations for efficient calculations on large datasets.
Implemented parallel processing for running multiple regressions simultaneously.

Robustness Checks:

Conducted sensitivity analyses with different estimation window lengths and event window specifications.
Implemented bootstrap methods for non-parametric significance testing.

Reporting:

Generated summary statistics and result tables using pandas DataFrame operations.
Developed functions for automated report generation, including key statistics and interpretations.



### Data Source & Structure:
Financial metrics data, including assets, liabilities, equity, and shares outstanding, along with current and non-current liabilities, are sourced from the SEC database. Specifically, for current S&P 500 constituents, data are obtained from [here](https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip). For removed historical S&P constituents, data are obtained using the SEC companyfact API: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json. All data files are in JSON format. All stock price data is downloaded using the yfinance package. 


### Executive Summary
The event study analyzing Donald Trump's 2016 election victory revealed complex and sometimes counterintuitive impacts on key stock market sectors. Contrary to expectations, the Energy sector underperformed despite Trump's pro-fossil fuel stance, showing negative abnormal returns particularly in the Fama-French model. The Financial sector, however, outperformed expectations, benefiting from anticipated deregulation policies. The Technology sector experienced slight underperformance, more pronounced in the Fama-French model. Notably, the Fama-French Three-Factor Model consistently showed more extreme abnormal returns compared to the simpler Market Model, highlighting the significance of size and value factors in explaining stock behavior with higher R squares. This discrepancy between models underscores the importance of employing multiple analytical approaches when assessing market reactions to political events. The study's findings emphasize that market responses to significant political changes are nuanced and not always aligned with headline policy promises, reflecting a complex interplay of sector-specific factors, existing market expectations, and broader economic considerations. This analysis provides valuable insights for investors and policymakers, suggesting the need for a multifaceted approach in predicting and interpreting market behavior in response to major political shifts.

### Results & Insights

Energy Sector:

Unexpectedly underperformed despite Trump's pro-fossil fuel stance.
Showed larger negative abnormal returns in the Fama-French model.
Displayed strong value characteristics but failed to capitalize on expected policy benefits.


Financial Sector:

Outperformed expectations, particularly in the Market Model.
Exhibited positive abnormal returns, aligning with anticipated deregulation.
Demonstrated the highest market sensitivity among the three sectors.


Technology Sector:

Slightly underperformed, more noticeably in the Fama-French model.
Showed characteristics more aligned with growth stocks.


Model Comparisons:

The Fama-French model generally revealed more extreme abnormal returns than the Market Model, highlighting the importance of considering size and value factors.


Market Reactions:
Varied impacts across sectors, not always aligning with initial policy expectations.
Financials benefited the most, while Energy underperformed contrary to expectations.



## Assumptions and Caveats:

Throughout the analysis, multiple assumptions were made to manage challenges with the data. These assumptions and caveats are noted below:

* Assumption 1: In the value-based factor project, due to limited dataset integrity from the SEC database, book value calculations are based on available metrics, discussed further in P1 and P4.

* Assumption 2: For the P/B ratio ranking, all negative values were omitted for various justifiable reasons, focusing only on low positive P/B ratios in the lowest 20% of the portfolio.
