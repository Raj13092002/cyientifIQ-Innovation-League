import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the Flipkart search results page
url = "https://www.flipkart.com/search?q=realme+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_10_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_10_na_na_ps&as-pos=2&as-type=RECENT&suggestionId=realme+mobile%7CMobiles&requestId=6ea618db-60f2-468a-bc6b-dc13fe87b72d&as-searchtext=realme%20mob"
# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product details on the page
    product_data = []

    # Find product details
    product_cards = soup.find_all('div', class_='_1AtVbE')

    for card in product_cards:
        # Extract data for each product


        try:
            brand = card.find('div', class_='_4rR01T').text.strip()
        except:brand="NaN"

        try:
            title = card.find('a', class_='IRpwTa').text.strip()
        except:title=""

        try:
            base_color = title.split(',')[0].strip()
        except:base_color=""

        try:
            model = title.split(',')[1].strip()
        except:model=""

        try:
            specs = card.find('ul', class_='_1xgFaf')
        except:specs=""

        try:
            specs_list = specs.find_all('li', class_='_21Ahn-')
        except:specs_list=""

        processor = ""
        screen_size = ""
        ROM = ""
        RAM = ""
        display_size = ""
        num_rear_camera = ""
        num_front_camera = ""
        battery_capacity = ""

        for spec in specs_list:
            text = spec.text.strip()
            if "Processor" in text:
                processor = text.split(":")[1].strip()
            elif "Screen Size" in text:
                screen_size = text.split(":")[1].strip()
            elif "ROM" in text:
                ROM = text.split(":")[1].strip()
            elif "RAM" in text:
                RAM = text.split(":")[1].strip()
            elif "Display Size" in text:
                display_size = text.split(":")[1].strip()
            elif "Rear Camera" in text:
                num_rear_camera = len(text.split(":")[1].strip().split(','))
            elif "Front Camera" in text:
                num_front_camera = len(text.split(":")[1].strip().split(','))
            elif "Battery Capacity" in text:
                battery_capacity = text.split(":")[1].strip()

        try:
            ratings = card.find('div', class_='_3LWZlK').text.strip()
        except:ratings=''
        try:
            num_of_ratings = card.find('span', class_='_2_R_DZ').text.strip()
        except:num_of_ratings=""
        try:sales_price = card.find('div', class_='_30jeq3').text.strip()
        except:sales_price=""

        try:discount_percent = card.find('div', class_='_3Ay6Sb').text.strip()
        except:discount_percent=""
        try:sales = card.find('div', class_='TbaEGU').text.strip()
        except:sales=""

        # Append the extracted data to the list
        product_data.append([
            brand, model, base_color, processor, screen_size, ROM, RAM, display_size,
            num_rear_camera, num_front_camera, battery_capacity, ratings, num_of_ratings,
            sales_price, discount_percent, sales
        ])

    # Save the data to a CSV file
    with open('flipkart_mobiles.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            'Brand', 'Model', 'Base Color', 'Processor', 'Screen Size', 'ROM', 'RAM',
            'Display Size', 'Number of Rear Cameras', 'Number of Front Cameras',
            'Battery Capacity', 'Ratings', 'Number of Ratings', 'Sales Price',
            'Discount Percent', 'Sales'
        ])  # Write header row
        csv_writer.writerows(product_data)  # Write product data rows

    print("Data saved to flipkart_mobiles.csv")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
