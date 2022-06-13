import requests
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dates = [date.strftime('%Y%m%d') for date in pd.date_range('2021-01-01', '2021-12-31')]
    api_url = lambda date: f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json'
    json_bank_data = [pd.read_json(requests.get(api_url(date)).text) for date in dates]

    df_bank_data = pd.concat(json_bank_data)

    df_bank_data.to_csv('s3://mysandoxbucket/lab4/currency_state_2021.csv')
    
    s3_df = pd.read_csv('s3://mysandoxbucket/lab4/currency_state_2021.csv')
    s3_df_USD = s3_df.query('cc == "USD"')
    s3_df_EUR = s3_df.query('cc == "EUR"')
    
    EUR_plot = s3_df_EUR[['exchangedate', 'rate']].plot(x = 'exchangedate', figsize=(16, 9))
    USD_plot = s3_df_USD[['exchangedate', 'rate']].plot(x = 'exchangedate', figsize=(16, 9))
    
    fig_EUR = EUR_plot.get_figure()
    fig_EUR.savefig('./EUR_plot.jpg')
    fig_USD = USD_plot.get_figure()
    fig_USD.savefig('./USD_plot.jpg')