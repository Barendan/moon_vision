from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

sheet_endpoint = "https://api.sheety.co/4fbe50a87952f1a22ec40a7a3da86ceb/moonVision/sheet1"

# Retrieve data and create local store
response_data = requests.get(sheet_endpoint)

if response_data.status_code == 200:
    coin_data = response_data.json()["sheet1"]
    # print(coin_data)
else:
    coin_data = []


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
coin_table = driver.find_elements(By.CSS_SELECTOR, ".cmc-table tr")[1:6]
coin_names = driver.find_elements(By.CLASS_NAME, "coin-item-symbol")[:6]

# Extract data from the top 10 coins & add to list
for item in coin_table:
    coin_info = item.text.split("\n")
    coin_rank = coin_info[0]
    coin_name = coin_info[2]
    coin_price = coin_info[3]
    # 1hr, 24hr, 7d % all together so need to be split into an array
    coin_perc = coin_info[4].split()[1]

    if float(coin_perc.rstrip("%")) > 25:
        top_coins.append({"rank": coin_rank, "name": coin_name, "price": coin_price, "increase": coin_perc})



# Compare new top coins to previous list and make new list
coin_names = set(c['name'] for c in top_coins)
updated_coins = [c for c in coin_data if not c['name'] in coin_names]
# print(coin_names)
print("NEW COINS:", updated_coins)

# delete_res = requests.delete(sheet_endpoint)



test_entry = {'rank': 2, 'name': 'Ethereum', 'price': 3566, 'increase': 0.30}
# sheet_response = requests.post(sheet_endpoint, json=updated_coins)
sheet_response = requests.post(sheet_endpoint, json={"sheet1": test_entry})
print(sheet_response.json())
# print({"sheet1": updated_coins})



# Check whether percentages are over 25%, 50%, or 100%
# for coin in top_coins:
#     if 50 > float(coin["increase"].rstrip("%")) > 25:
#         new_coins.append(coin)
#     # if float(coin["increase"].rstrip("%")) > 50:

driver.quit()














# Run check twice per day at 6am and 6pm
# today_date = datetime.now().strftime("%d/%m/%Y")
# now_time = datetime.now().strftime("%X")


# If not same coin as last time, send text message with coin details



