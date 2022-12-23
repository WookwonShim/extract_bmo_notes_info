import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the class_name to find the specific table containing the product details.
class_name = "display compact SellingTable dataTable no-footer"
# Set the label name to find the specific table head containing the information.
label_name = "aria-label"

# A function that takes a list of JHN Codes as an argument and returns the product detiails in a Pandas DataFrame.
def extract_data(jhn_codes):
    df_list = []  # list to store DataFrames
    for jhn_code in jhn_codes:

        url = f"https://www.bmonotes.com/Note/Info/{jhn_code}" # The URL.
        data = {} # A dictionary to store label-value pairs.
        
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the table element (a class name to find for the table == class_name)
        table_element = soup.find("table", class_= class_name)
        # Find all table rows in the table element.
        tr_elements = table_element.find_all("tr")

        for tr in tr_elements:
            th_element = tr.find("th")
            if th_element:
                label = th_element.get(label_name)
                if not label:
                    label = th_element.get_text().strip()  # get label from th element
                td_element = tr.find("td")
                if td_element:
                    value = td_element.get_text().strip()  # get value from td element
                    data[label] = value

        df_list.append(pd.DataFrame([data]))  # add DataFrame to list

    df = pd.concat(df_list)  # combine DataFrames into one
    return df

jhn_codes = ["JHN15000", "JHN15001"]  # list of JHN codes
df = extract_data(jhn_codes)  # extract data for the notes. 

df
