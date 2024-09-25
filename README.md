# Event Study Project (P7): Trump's Presidency Impact on Stock's Abnormal Returns - "Is there any alpha?"
## Background
"What does it mean for the stock market if Donald Trump is re-elected as President of the United States?" This question is stirring much debate as the election approaches, with Vice President Kamala Harris and Donald Trump competing for the presidency. Understanding past events—like the market's reaction in 2016—is crucial to foreseeing the possible impacts of Trump’s potential re-election. Did the market already factor in expected policy changes such as deregulation, tax cuts, and new trade policies affecting sectors like Banking, Energy, and Construction, or is there room to generate alphas based on election results? This project aims to peel back the layers of market reactions to uncover deeper insights. (*Note while this project uses Trump's 2016 election as an event example, the methodology and code provided here is applicable to any event studies)

**Key Areas of Focus Include:**
- **Model Comparison**: Analyzing differences between the Market Model and the Fama-French Three-Factor Model to forecast returns, emphasizing the importance of factor selection on estimation.
- **Statistical Analysis**: Reviewing return metrics, t-statistics, and p-values to measure the significance of abnormal returns, using OLS regression for model parameter estimation. 
- **Sector Analysis**: Examining how Trump's election and the market's anticipation of policy changes influence sector-specific returns, particularly in Financials, Energy, and Technology.   
- **Factor Exposures For Various Sectors**: Discussing the factor exposure across Financial, Energy, and Technology sectors.
- **Event Windows Analysis**: Detailing returns across different event windows to understand market dynamics during key election periods.
  
### Strategy Design Methodology:
- **Event Study Timeline**: in this study, two sets of timeline parameters are applied. The initial set consists of an estimation period of 100 trading days, a 50-day gap period, and a 20-day event window (10 days before and after the event). The gap serves to prevent information leakage by separating the estimation period from the event window (estwin=100, gap=50, evtwins=-10, evtwine=10). The second set consists of the same length of estimation and gap period, with event window expanding to 40 days (20 days before and after the event respectively). 2016-11-09 is set as the event date for the analysis. The timeline is as followed: ![event_study_timeline](https://github.com/user-attachments/assets/255dec7c-7cd8-4c49-a876-206dd4c136f3)
- **Risk Model Estimation**: The study applies two risk models, the Fama-French and Market models, to compute the alphas and betas through OLS regression.
- **Return and Volatility Metrics**: The analysis employs various return metrics to evaluate the results, including Abnormal Returns (AR), Buy-and-Hold Abnormal Returns (BHAR), and Standardized Abnormal Returns (SAR), along with their cumulative returns and volatilities.

### Techniques used in this Event Study project:
Data Collection and Preparation:
- Utilized complex SQL queries to extract stock return data and factor returns from CRSP and Fama-French databases. (i.e. window, case, coalesce functions etc.) 
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
- Used seaborn to create heatmaps to visualize cross-sectional abnormal returns across different event window days.

### Data Source & Structure:
CRSP and Fama-French libraries

### Executive Summary
The event study analyzing Donald Trump's 2016 election victory revealed complex and sometimes counterintuitive impacts on key stock market sectors. Contrary to expectations, the Energy sector underperformed despite Trump's pro-fossil fuel stance, showing negative abnormal returns particularly in the Fama-French model. The Financial sector, however, outperformed expectations, benefiting from anticipated deregulation policies. The Technology sector experienced slight underperformance, more pronounced in the Fama-French model. Notably, the Fama-French Three-Factor Model consistently showed more extreme abnormal returns compared to the simpler Market Model, highlighting the significance of size and value factors in explaining stock behavior with higher R squares. This discrepancy between models underscores the importance of employing multiple analytical approaches when assessing market reactions to political events. The study's findings emphasize that market responses to significant political changes are nuanced and not always aligned with headline policy promises. Sector-specific factors, existing market expectations, and broader economic condition all play a significant part in it.

### Results & Insights

Model Comparisons:
- The Fama-French model generally revealed more extreme abnormal returns than the Market Model, highlighting the importance of considering size and value factors. Below is the summary snapsht on the last day of the event window across sectors and models under the 20-day event window.  
![last_event_day](https://github.com/user-attachments/assets/e444319d-a0c6-4237-abcd-bab8b2cade3a)

- By extending the event window from 20 days (above) to 40 days (below), both the Cumulative Abnormal Returns (CAR) and Buy-and-Hold Abnormal Returns (BHAR) showed improvements across sectors using the market model. However, these abnormal returns declined under the Fama-French model. Both beta and alpha remained relatively stable under both models and across the different event windows, demonstrating consistent sector factor exposures.

  ![last_event_day_40](https://github.com/user-attachments/assets/3054b82c-cb0e-4104-be7c-b11c8d16b7fc)

- On a more granular level, a breakdown of all the companies within a specific sector using a particular model is provided in the analysis. Below is an example of the summary from the last event day for companies in the Financials sector under the Fama-French model.
![last_event_day_breakdown](https://github.com/user-attachments/assets/7eb8e5bf-f252-47cd-aecb-34003cfee936)

Energy Sector:
- Unexpectedly underperformed despite Trump's pro-fossil fuel stance.
- Showed larger negative abnormal returns in the Fama-French model.
- Displayed strong value characteristics but failed to capitalize on expected policy benefits.
![energy_ff](https://github.com/user-attachments/assets/54016ca4-c271-484f-87ff-bea8315cc818)
![energy_Market](https://github.com/user-attachments/assets/3e73a7f7-e2a7-4429-90c2-3658053cda47)

Financial Sector:
- Outperformed expectations, particularly in the Market Model.
- Exhibited positive abnormal returns, aligning with anticipated deregulation.
- Demonstrated the highest market sensitivity among the three sectors.
![financials_ff](https://github.com/user-attachments/assets/4bcf75d4-a603-4844-a503-7a5b9899ca02)
![financials_Market](https://github.com/user-attachments/assets/8752f666-0b94-4b7b-b909-1943b0662a25)

Technology Sector:
- Slightly underperformed, more noticeably in the Fama-French model.
- Showed characteristics more aligned with growth stocks.
![technology_ff](https://github.com/user-attachments/assets/49e12fdb-6436-4a89-876f-18d9f527da91)
![technology_Market](https://github.com/user-attachments/assets/ceb63465-91a1-4ba8-93f5-285dfcff0fdc)


**Implications:** The study shows that the market response to Trump's election was more complex than just the effects of his policy announcements.Factors such as market expectations, sector-specific dynamics, and broader economic conditions also played significant roles. Moreover, the variation in results across different models highlights the importance of employing multiple analytical approaches to fully grasp the financial impact of such events. Based solely on this event study, a recommended strategy would be to invest in financial stocks if Trump were to be re-elected.

### References

Boehmer, E., Poulsen A., and Musumeci, J., 1991. Event Study Methodology Under Conditions of Event-Induced Variance, Journal of Financial Economics, 30.

Boehmer, E., Broussard, P. and Kallunki, J-P., 2002. Using SAS© in Financial Research. Cary, NC: SAS Institute Inc.

Kothari, S.P. and Warner, J.B., 2006. The Econometrics of Event Studies, published in Handbook of Corporate Finance: Empirical Corporate Finance, Volume A, Ch. 1.

MacKinlay, Craig, 1997. “Event Studies in Economics and Finance”, Journal of Economic Literature, Vol. 35, No. 1, pp.13-29.



