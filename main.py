from selenium import webdriver
from selenium.webdriver.common.by import By
from twilio.rest import Client
import time
import pygsheets
import pandas as pd

# Connect GSheets and import relevant data
# gc = pygsheets.authorize(service_file="/Users/Daniel/Desktop/Python_Pies/Moon_vision/creds.json")
gc = pygsheets.authorize(service_file="/home/Barendan/moon_vision/creds.json")
sh = gc.open_by_key('1r64yJ-pb5A7JDa8ioBo079lKbWGXVEe8-Bs4kLUT0Qc')
wks = sh.sheet1

crypto_df = wks.get_as_df()
yesterday_coin_list = crypto_df.to_dict(orient='records')
print(yesterday_coin_list)


driver = webdriver.Chrome()
driver.get("https://coinmarketcap.com/")

# Wait for page to load
time.sleep(3)

# Find 24hour button and click to sort all the coins
sort24 = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/thead/tr/th['
                                        '6]/div/div/p')
sort24.click()

# Retrieve info on top ten coins after being sorted
top_coins = []
coin_table = driver.find_elements(By.CSS_SELECTOR, ".cmc-table tr")[1:11]
coin_names = driver.find_elements(By.CLASS_NAME, "coin-item-symbol")[:11]


# Extract data from the top 10 coins & add to list
for item in coin_table:
    coin_info = item.text.split("\n")
    coin_rank = coin_info[0]
    coin_name = coin_info[1]
    coin_sym = coin_info[2]
    coin_price = float(coin_info[3].split("$")[1].replace(',', ''))
    # 1hr, 24hr, 7d % all together so need to be split into an array
    coin_perc = coin_info[4].split()[1]

    print(coin_name)

    if float(coin_perc.rstrip("%")) > 25:
        top_coins.append({"rank": coin_rank, "name": coin_name, "symbol": coin_sym, "price": coin_price, "increase": coin_perc})

wks.set_dataframe(pd.DataFrame(top_coins), start='A1')
# print(pd.DataFrame(top_coins))

# Send text message with coin details


def send_message():
    account_sid = 'AC9464cf4fd176a7736b920ac9d1aa601d'
    auth_token = 'e3f13a3e76494cd2afa4767db21f6fd8'
    twilio_phone_number = '+18777214880'
    your_phone_number = '+13053067522'

    client = Client(account_sid, auth_token)

    message_body = "\nLaunched:\n"
    for coin in top_coins:
        message_body += f"{coin['rank']}:{coin['name'][:8]} ({coin['symbol']}) ${'{:.8f}'.format(coin['price'])} ^^{coin['increase']}\n"

    print(message_body)

    message = client.messages.create(
        to=your_phone_number,
        from_=twilio_phone_number,
        body=message_body
    )

send_message()


# Compare new top coins to previous list and make new list
# today_top_coins = set(c['name'] for c in top_coins)
# print("Today's TOP:", today_top_coins)
# updated_coins = [c for c in yesterday_coin_list if not c['name'] in today_top_coins]
# print("NEW COINS:", updated_coins)


# Check whether percentages are over 25%, 50%, or 100%
# for coin in top_coins:
#     if 50 > float(coin["increase"].rstrip("%")) > 25:
#         new_coins.append(coin)
#     # if float(coin["increase"].rstrip("%")) > 50:

driver.quit()
