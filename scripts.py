import pandas as pd
import requests
headers = {"User-Agent": "ian.ye.fu@gmail.com"} 

data_folder_download = './datasets/download/'
data_folder_generate = './datasets/generate/'

def cik_matching_ticker(ticker, headers=headers):
    ticker = ticker.upper().replace(".", "-")
    ticker_json = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()

    for company in ticker_json.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            return cik
    raise ValueError(f"Ticker {ticker} not found in SEC database")


def get_fiscal_YE(sp500_cik_list):
    """
    Get_fiscal_year_end for S&P companies by passing the cik list.
    """
    fiscal_YE = []
    
    for cik in sp500_cik_list:
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        
        try:
            # Make the API request
            company_json = requests.get(url, headers=headers).json()
            
            # Check if 'fiscalYearEnd' exists in the JSON response
            fiscal_year_end = company_json.get('fiscalYearEnd', 'N/A')
            
            # Append the result
            fiscal_YE.append(fiscal_year_end)
            
        except Exception as e:
            # In case of error, append 'N/A' or handle accordingly
            print(f"Error fetching data for CIK {cik}: {e}")
            fiscal_YE.append('N/A')
            
    return fiscal_YE



def get_facts(ticker, sp500_df, headers):
    """
    Load company_facts data from SEC API
    """
    try:
        cik = f'CIK{sp500_df.loc[ticker, "CIK"]}'
        url = f"https://data.sec.gov/api/xbrl/companyfacts/{cik}.json"
        response = requests.get(url, headers=headers)
        
        # Check if the response status code is 200 (success)
        if response.status_code == 200:
            company_facts = response.json()
            return company_facts
        else:
            print(f"Error: {response.status_code} for ticker {ticker}. Skipping.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}. Skipping ticker {ticker}.")
        return None



def facts_DF(ticker, sp500_df, headers=headers):
    """
    Convert the company_facts dict to dataframes
    """
    facts = get_facts(ticker, sp500_df, headers)  # get company facts data
    
    # Check if facts is None before processing
    if facts is None:
        print(f"No data available for {ticker}. Skipping...")
        return pd.DataFrame()
    
    # Process us_gaap data
    us_gaap_data = facts.get("facts", {}).get("us-gaap", {})
    df_data = []
    
    for fact, details in us_gaap_data.items():
        for unit in details.get("units", {}).keys():
            for item in details["units"][unit]:
                row = item.copy()  # keep the original data intact
                row["fact"] = fact
                row["label"] = details["label"]
                df_data.append(row)
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(df_data)
    
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])
    
    df = df.drop_duplicates(subset=["fact", "end", "val"])
    df.set_index("end", inplace=True)
    
    labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
    
    return df



def download_financial_data_from_SEC(sp500_tickers, sp500_df, data_category, headers = headers):
    """
    download all the financial metrics in the data_category from SEC for the sp500 companies 
    """
    sp500_financial_data = {} # outer dict
    
    for ticker in sp500_tickers:
        
        df = facts_DF(ticker, sp500_df, headers)  # Correct data extraction for the ticker
        financial_data= {} # inner dict
        
        # Loop over all categories in the data_category list
        for category in data_category:
            
            x = df.query('fact == @category')
            x = x[(x['val']!= 0) & (x['val'].notna())]
            # remove the duplicated rows based on 'end' index and keep the last record
            cleaned_data = x[~x.index.duplicated(keep='last')].sort_index(ascending = True)
            # slice data from only 2013 onwards
            financial_data[category] = cleaned_data.loc['2013':]  
            
        # Assign the financial data for each ticker
        sp500_financial_data[ticker] = financial_data
        
    return  sp500_financial_data


def convert_annual_to_quarter(sp500_financial_data, updated_data_category):
    """
    This function updates financial data by subtracting the annual rows by 
    the sum of the previous three quarters for a given list of tickers and data categories
    """
    
    for ticker in sp500_financial_data.keys(): 

        for category in sp500_financial_data[ticker].keys(): 
            
            new_df = sp500_financial_data[ticker][category].reset_index().copy() 

            if category == "EarningsPerShareDiluted" or category == 'CommonStockDividendsPerShareDeclared' or category == 'NetIncomeLoss':

                # identify the annual rows
                index_list = new_df[(new_df['end'] - new_df['start']).dt.days > 130].index.tolist()
    
                # subtract the annual rows by the sum of the previous three quarters.
                for i in index_list: 
                    new_df.loc[i,'val'] = new_df.loc[i,'val'] - new_df.loc[i-3: i-1, 'val'].sum()
    
            sp500_financial_data[ticker][category] = new_df.set_index('end')
        
    return sp500_financial_data


def weighting(metric_ranking_df, monthly_availability_df): 
    """
    Calculate the weighting among selected stocks to construct the portfolio for each month
    Select the top 20% and bottom 20% stocks based on ranking and assign equal weights between the stocks. 
    """
    # filter the PB ranking df based on the monthly availability of the stocks.
    filtered_metric_ranking_df = metric_ranking_df*monthly_availability_df

    # Calculating the top and bottom 20% of the companies for each month: 
    top_20_threshold = filtered_metric_ranking_df.quantile(0.8, axis=1)
    bottom_20_threshold = filtered_metric_ranking_df.quantile(0.2, axis=1)

    # Create masks for top 20% and bottom 20%
    top_20_mask = filtered_metric_ranking_df.ge(top_20_threshold, axis=0)
    bottom_20_mask = filtered_metric_ranking_df.le(bottom_20_threshold, axis=0)

    # Filter dataframes for top 20% and bottom 20%
    top_20_df = filtered_metric_ranking_df[top_20_mask]
    bottom_20_df = filtered_metric_ranking_df[bottom_20_mask]

    # Calculate equal weight for each stock in top 20% and bottom 20%
    top_20_weights = 1 / top_20_df.count(axis=1)
    bottom_20_weights = 1 / bottom_20_df.count(axis=1)

    # Apply the weights across the dataframe. 
    top_20_df_weights = top_20_df.map(lambda x: 1 if pd.notna(x) else np.NaN).multiply(top_20_weights, axis=0)
    bottom_20_df_weights = bottom_20_df.map(lambda x: 1 if pd.notna(x) else np.NaN).multiply(bottom_20_weights, axis=0)

    return top_20_df_weights, bottom_20_df_weights


def cal_cum_rets(top_20_df_weights, bottom_20_df_weights, monthly_returns_df): 
    
    value_20130331 = 100
    # Multiply the monthly returns by the equal weights and aggregate monthly returns. 
    top_20_weighted_monthly_returns = ((top_20_df_weights.shift(1) * monthly_returns_df).sum(axis = 1)).iloc[1:]
    bottom_20_weighted_monthly_returns = ((bottom_20_df_weights.shift(1) * monthly_returns_df).sum(axis = 1)).iloc[1:]
    long_short_monthly_returns =  bottom_20_weighted_monthly_returns - top_20_weighted_monthly_returns
    
    top_20_weighted_cum_returns = value_20130331*(1 + top_20_weighted_monthly_returns).cumprod() - 1
    bottom_20_weighted_cum_returns = value_20130331*(1 + bottom_20_weighted_monthly_returns).cumprod() - 1
    long_short_cum_returns = value_20130331*(1 + long_short_monthly_returns).cumprod() - 1

    return  top_20_weighted_cum_returns, bottom_20_weighted_cum_returns, long_short_cum_returns


def cal_index_cum_rets(index_name, data_folder_download): 
    
    value_20130331 = 100
    index_price = pd.read_csv(data_folder_download + index_name + '.csv', index_col = "Date", parse_dates = True)
    index_price = index_price.resample('ME').last()
    
    index_monthly_returns = index_price / index_price.shift(1) - 1
    index_monthly_returns = index_monthly_returns.iloc[3: ] 
    index_cum_returns = value_20130331*(1 + index_monthly_returns).cumprod() - 1

    return index_cum_returns

def calc_rolling_12mon_return_n_vol(monthly_return):
    """
    calculate the rolling 12month returns and volatilities of a given monthly_return series
    """
    rolling_12mon_return = (1 + monthly_return).rolling(window = 12).apply(lambda x: x.prod()) - 1
    rolling_12mon_std = rolling_12mon_return.rolling(window = 12).std()*np.sqrt(12)
    return rolling_12mon_return, rolling_12mon_std


def calc_index_monthly_returns(ticker, folder):
    index_price = pd.read_csv(folder + ticker + '.csv', index_col = "Date", parse_dates = True)
    index_price = index_price.resample('ME').last()
    index_monthly_returns = index_price / index_price.shift(1) - 1 
    return index_monthly_returns


def get_10Y_bond_yields(folder, file, syear, smonth, sday, eyear, emonth, eday): 
    """
    Get the US 10Y government bond yield
    """
    # read the file into a dataframe
    df = pd.read_csv(data_folder_download + file + '.csv', index_col = 'DATE', parse_dates = True).rename(columns = {'DGS10': '10YR'})
    df['10YR'] = pd.to_numeric(df['10YR'], errors = 'coerce')
    df['10YR'] = df['10YR']/100
    # convert datetime
    start = f"{syear}-{smonth}-{sday}"
    start = pd.to_datetime(start) 
    end = f"{eyear}-{emonth}-{eday}"
    end = pd.to_datetime(end)
    # select the timespan
    df = df.loc[start:end]
    return df

def sharpe_ratio(r, riskfree_rate, periods_per_year):
    """
    Compute the annualized sharpe ratio of a set of returns
    """
    length = r.shape[0]
    riskfree_rate = pd.Series(riskfree_rate, index = r.index)
    rf_per_period = (1+riskfree_rate)**(1/periods_per_year)-1
    rf_per_period = rf_per_period.iloc[3:]
    excess_ret = r - rf_per_period
    annualized_ret = (excess_ret + 1).prod() ** (periods_per_year/length) - 1
    annualized_vol = excess_ret.std()*(periods_per_year**0.5)
    
    return annualized_ret/annualized_vol


def drawdown(return_series: pd.Series):
    """
       Takes a time series of asset returns.
       returns a DataFrame with columns for
       the wealth index, 
       the previous peaks, and 
       the percentage drawdown
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({"Wealth": wealth_index, 
                         "Previous Peak": previous_peaks, 
                         "Drawdown": drawdowns})

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

def var_historic(r, level):
    if isinstance(r, pd.DataFrame):
        return r.aggregate(lambda x: abs(np.percentile(x, level)), axis = 0)
    elif isinstance(r, pd.Series): 
        return abs(np.percentile(r, level))  # note here I only want the scaler without index for further comparison or masking. 
    else:
        raise TypeError("Expected r to be Series or DataFrame")


from scipy.stats import norm
def var_gaussian(r, level=5, modified=False):
    """
    Returns the Parametric Gauusian VaR of a Series or DataFrame
    If "modified" is True, then the modified VaR is returned,
    using the Cornish-Fisher modification
    """
    # compute the Z score assuming it was Gaussian
    z = norm.ppf(level/100)
    if modified:
        # modify the Z score based on observed skewness and kurtosis
        s = skewness(r)
        k = kurtosis(r)
        z = (z +
                (z**2 - 1)*s/6 +
                (z**3 -3*z)*(k-3)/24 -
                (2*z**3 - 5*z)*(s**2)/36
            )
    return -(r.mean() + z*r.std(ddof=0))

def cvar_historic(r, level=5):
    """
    Computes the Conditional VaR of Series or DataFrame
    """
    if isinstance(r, pd.Series):
        var_value = var_historic(r, level=level)
        is_beyond = r<= -var_value
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level = level)
    else:
        raise TypeError("Expected r to be a Series or DataFrame")