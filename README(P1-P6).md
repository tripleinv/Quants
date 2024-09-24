# Factor-based Quantitative Strategies Projects (P1-P6)
## Background
Factor investing has become increasingly popular among both passive and active investors due to its incorporation of various strategies such as value, growth, size, momentum, quality, and risk. This repository highlights two main projects focusing on factor-based investment strategies that leverage value and growth. The first project is centered on a value-based factor portfolio strategy utilizing the Price-to-Book (P/B) ratio. The second project emphasizes a growth-based factor portfolio strategy that capitalizes on earnings surprises.

**Insights and recommendations are provided on the following key areas:**
- **Factor-based Portfolio Construction**: Constructing value factor (P/B ratio) and growth factor (earnings surprise) based portfolios among the S&P 500 indexes from 2013 to current, focusing on selecting relevant stocks by calculating and ranking these factors and assinging correponding weightings.
- **Backtesting Returns Analysis**: Evaluating the historical performance of these portfolios against both equally-weighted and market-cap-weighted S&P 500 indices.
- **Risk and Return Characteristic**s: Analyzing the rolling 12-month annual return and rolling 12-month standard deviation among the portfolios compared to benchmarks.
- **Performance Metrics Assessment**: Providing a detailed review of key performance indicators such as the Sharpe Ratio, Maximum Drawdown, Value at Risk (VaR), and Conditional Value at Risk (CVaR).
- **Factor Sector Concentration Analysis**: Offering an overview of the sector distribution within the portfolios, highlighting predominant sectors in each strategy.  


**Techniques used in these projects:**

Data Collection Techniques:
- Employed web scraping and API requests to acquire company tickers and financial information from resources such as the SEC database, Wikipedia, and YahooFinance. 
- Leveraged SQL for interactions with several databases like Compustat, CRSP, and I/B/E/S.
- Utilized the requests library for API interactions and processed data from JSON files.

Data Manipulation and Processing:
- Time Series Data Handling: Utilized pandas for resampling and aligning time series data to consistent intervals, employing various timeseries functions such as pd.tseries.offsets.MonthEnd().rollforward(), resample(), and dt.days
- Data Cleaning and Transformation: Cleaned and restructured data using groupby(), and merge(). Addressed data anomalies and missing data effectively through functions like fillna(), describe(), qcut(), sort_values(), value_counts(), and unique().
- Data Analysis and visualization: Implemented complex Python operations including rolling window calculations, lambda functions, apply(), map(), and np.where(). Enhanced data structure management by leveraging list comprehensions, set operations, and dictionary manipulations. Handled sophisticated data frameworks like dictionaries of lists/dictionaries, DataFrames, and multi-indexed DataFrames with operations like pivot() and stack() to structure and analyze data efficiently.

Financial Metrics Calculation:
- Computed several financial metrics such as annualized returns/volatility, price-to-book value per share, earnings surprise, Sharpe Ratio, Max Drawdown, Value at Risk (VaR), Conditional Value at Risk (CVaR), Skewness, and Kurtosis.


## Value-Based Factor Portfolio Strategy (P1 - P5)
### Overview
The value-based strategy project aims to construct portfolios by ranking stocks based on their P/B ratios. Lower P/B ratios are assumed to indicate undervalued stocks, which are targeted for the "high value" portfolio. The project involves data acquisition, cleaning, analysis, and backtesting to assess the performance of the strategy over several years. Price/Book Value is calculated as Month-end price divided by latest reported book value per share. The analysis also includes all the removed tickers historically from the S&P 500 index components since 2013 to eliminate the survivorship bias. 

### Data Source & Structure:
Financial metrics data, including assets, liabilities, equity, and shares outstanding, along with current and non-current liabilities, are sourced from the SEC database. Specifically, for current S&P 500 constituents, data are obtained from [here](https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip). For removed historical S&P constituents, data are obtained using the SEC companyfact API: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json. All data files are in JSON format. All stock price data is downloaded using the yfinance package. 

### Strategy Design Methodology:
- Price/Book Value is calculated as Month-end price divided by latest reported book value per share
- Rank stocks on a monthly basis based on Price/Book Value while excluding the stocks with negative P/B value.
- Construct portfolios from the top 20% and bottom 20% of stocks with equal weightings based on P/B ratio.

### Executive Summary
This project's findings reveal that value-driven investment strategies, especially those employing low P/B ratios, have lagged behind their high P/B counterparts in recent years. This performance gap was particularly pronounced during the 2020 pandemic lockdown, where the low P/B strategy faltered significantly. Generally, in times of economic recession, investors tend to favor higher-quality stocks that often command a premium in terms of their price-to-book values. Despite these recent trends, both high and low P/B strategies have consistently outperformed the S&P 500 benchmark over the last ten years. In terms of risk versus reward, the high P/B strategy yielded the highest returns with relatively moderate risks compared to the low P/B strategy. From a sectoral perspective, the financial sector has predominantly characterized the low P/B strategy, with energy also playing a significant role.

### Results & Insights

Cumulative Returns of Low and High P/BVPS Strategy:

- The High Price/BVPS Strategy exhibits consistent long-term growth over the past decade, outperforming the Low Price/BVPS strategy and the S&P Equal Weight and Market-Cap Weighted 500 Index. This outperformance becomes prominent from 2018 onwards. 

![cumulative_returns_of_low_and_high_PBVPS_strategy](https://github.com/user-attachments/assets/8a2fe9b0-7fef-410a-b69c-de21c7dc9072)

Relative Performance of Low P/B, High P/B to S&P 500 Indexes: 
- The long-short Price/BVPS spread indicates increasing profitability of betting on high P/B while shorting low P/B stocks, especially during the time of economic recession and increased market volatility, as shown noticeablely post-2020.

![relative_performance_of_low_pb_high_pb](https://github.com/user-attachments/assets/a4618e12-2ffc-4965-a8b6-c5ddbe12be83)

Risk and Return Characteristics: 
- The Long high P/B strategy showcases superior risk-adjusted returns, with lower volatility and higher average returns than the S&P 500 and Equal Weight S&P 500. 

![low pb value risk reward characteristics](https://github.com/user-attachments/assets/2789247b-b5fa-446c-8e11-4ee9862f50a0)

Risk Performance Metrics:

![risk matrics](https://github.com/user-attachments/assets/753bb904-19a8-4787-87d3-72a783bcfa12)

Low Price/Book Value Sector Concentration:
- Financials has counted as the major sector under the P/BVPS value factor over the last decade, with Utilities and Consumer Staples seeing an increasing factor exposure post the covid. 

![low_pb_value_sector_concentration](https://github.com/user-attachments/assets/57ab82fd-6599-42f8-8288-8a335e19ad6e)


--------------------------------------------------------------------------------------------------------------------------------------------

## Growth-Based Factor Portfolio Strategy (Earnings Surprise, P6)
### Overview
This project calculates earnings surprise based on the street's consensus to create a growth-based factor portfolio that aims to capitalize on the market's reaction to earnings reports. The strategy is inspired by the research conducted on PEAD (Post Earnings Announcement Drift), which stated the tendency for a stock’s cumulative abnormal returns to drift in the direction of an earnings surprise for several weeks (even several months) following an earnings announcement. The earnings surprise is calcualted as the difference between the actual reported earnings per share and the most recent I/B/E/S street's consensus divided by the most recent street's consensus. 

### Data Source & Structure:
Financial data for stocks is sourced from Compustat, while pricing data is acquired from CRSP, and earnings estimates are retrieved from I/B/E/S. These datasets are accessed and integrated using SQL queries. Key identifiers such as gvkey, CIK, CUSIP, permno, and permco are utilized to consolidate the datasets. For further details, refer to notebook P6.

### Strategy Design Methodology:
- Filter for the most recent quarterly earnings estimates and actuals before the announcement date.
- Calculate the decay factor of earnings surprises to lessen the weights of older surprises.
- Construct monthly earnings surprise factors and rebalance portfolios accordingly on a monthly basis.
- Construct portfolios from the top 20% and bottom 20% of stocks with equal weightings based on earnings surprises.

### Executive Summary
The strategy centered on earnings surprises, particularly those that are positive, demonstrates a robust capability to secure additional returns following earnings announcements. In the last ten years, strategies employing long positions on positive earnings surprises have not only surpassed negative earnings surprise strategies but also outperformed the broader S&P 500 indices. This approach tends to exhibit increased volatility; however, this is balanced by correspondingly higher returns. Analysis of the Sharpe Ratio reveals that the long positive earnings surprise strategy achieves a 56% rate, outdoing the 48% rate seen with negative earnings surprises. Nonetheless, this strategy also highlights the critical need for precise timing and swift action, as the impact of such surprises tends to fade quickly.

### Results & Insights

Cumulative Returns Chart:

- The Positive Surprise Strategy surpasses both the Negative Surprise Strategy and the S&P 500 index, showing robust growth especially post-2016.
The Negative Surprise Strategy occasionally underperforms the market, suggesting a riskier proposition.

![cumulative returns of positive and negative earnings surprise](https://github.com/user-attachments/assets/e2def168-c8dd-4011-b639-0c7ec01e9585)

Relative Performance Chart:

- Both strategies have varied in performance relative to the S&P 500, with the Positive Surprise Strategy demonstrating considerable outperformance since 2018, underscoring its effectiveness during varying market conditions. The Long-Short Earnings Surprise Spread shows periods of significant divergence after 2020, indicating potential tactical opportunities within a broader strategic framework.

![relative performance of negative and positive earnings surprise](https://github.com/user-attachments/assets/741e6665-1d69-4fd3-9f20-71afaab0303a)

Risk-Reward Characteristics Chart:

- The Positive Surprise Strategy exhibits higher average returns with a risk profile only marginally higher than the S&P 500, denoting an attractive risk-reward balance. The Negative Surprise Strategy shows higher variability in returns, implying increased risk without commensurate reward.
![long positive and negative earnings surprise value risk reward](https://github.com/user-attachments/assets/47c4df31-141b-480e-b6b3-ced473d86ea1)

Risk Performance Metrics:

![risks matrcis](https://github.com/user-attachments/assets/97e8f8d5-46d1-4175-81e0-ae817328cfe7)

Sector Concentration Chart:

- The sector distribution for investments based on positive earnings surprises has remained diverse, with noticeable shifts in sector weightings over the years, reflecting adaptive strategy allocations.

![positive earnings surprise factor sector concentration](https://github.com/user-attachments/assets/13f14548-9be4-4614-aaf6-c1e88a56750d)


## Assumptions and Caveats:

Throughout the analysis, multiple assumptions were made to manage challenges with the data. These assumptions and caveats are noted below:

* Assumption 1: In the value-based factor project, due to limited dataset integrity from the SEC database, book value calculations are based on available metrics, discussed further in P1 and P4.

* Assumption 2: For the P/B ratio ranking, all negative values were omitted for various justifiable reasons, focusing only on low positive P/B ratios in the lowest 20% of the portfolio.
  
* Assumption 3: In the growth-based factor project, factor decay is calculated by multiplying the number of days post-announcement by -1.5%, based on the hypothesis from Bernard and Thomas (1990), suggesting that the stock price reaction does not completely reflect the impact of current earnings on future earnings.

* Assumption 4: All portfolio constructions are based on an unconstrained approach, excluding real-life implementation costs such as transaction fees.
