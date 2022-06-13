import requests
import pandas as pd
import matplotlib.pyplot as plt

def download_data():
    dates = [date.strftime('%Y%m%d') for date in pd.date_range('2021-01-01', '2021-12-31')]
    api_url = lambda date: f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json'
    json_bank_data = [pd.read_json(requests.get(api_url(date)).text) for date in dates]
    df_bank_data = pd.concat(json_bank_data)
    df_bank_data.to_csv('./currency_2021.csv', index = False)

def plot_images():
    df_bank_data = pd.read_csv('./currency_2021.csv')
    df_bank_data_USD = df_bank_data.query('cc == "USD"')
    df_bank_data_EUR = df_bank_data.query('cc == "EUR"')

    EUR_plot = df_bank_data_EUR[['exchangedate', 'rate']].plot(x = 'exchangedate', figsize=(16, 9))
    USD_plot = df_bank_data_USD[['exchangedate', 'rate']].plot(x = 'exchangedate', figsize=(16, 9))

    fig_EUR = EUR_plot.get_figure()
    fig_EUR.savefig('./EUR_plot.jpg')
    fig_USD = USD_plot.get_figure()
    fig_USD.savefig('./USD_plot.jpg')

def main():
    download_data()
    plot_images()

if __name__ == "__main__":
    main()