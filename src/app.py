import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
from io import StringIO
#Step 2: Download HTML
# The HTML of the web page will be downloaded using the requests library, as we saw in the module's theory.

# The web page we want to scrape is the following: https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify. Collect and store the scraped text from the web in a variable.
url = "https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify"
resposta = requests.get(url)
if resposta:
    soup = BeautifulSoup(resposta.text, 'html.parser')
    scraped = soup.get_text()


# Step 3: Transform the HTML
# Using BeautifulSoup, analyze the HTML to find the structure containing the data (e.g., <table>, <li>, <div>, etc.).

# If you are using Wikipedia and it contains a table, you can directly use pandas.read_html() to load it as a DataFrame.

tabela = soup.find("table", class_="wikitable")
df = pd.read_html(StringIO(str(tabela)))
df = df[0]
print(df)




# Step 4: Process the DataFrame
# Next, clean the rows to obtain clean values by removing $ and B. Also, remove any rows that are empty or lack information.
df_string = df.astype(str)
for coluna in df_string.columns:
    df_string[coluna] = df_string[coluna].str.replace('$', '', regex=False)

df_string["Streams (billions)"] = df_string["Streams (billions)"].str.replace('B', '', regex=False)

df_limpo = df_string 
df_limpo["Streams (billions)"] = pd.to_numeric(df_limpo["Streams (billions)"], errors='coerce')

print(df_limpo)



# Step 5: Store the data in SQLite
# Create an empty database instance and include the cleaned data in it, as we saw in the database module. Once you have an empty database:

# Create the table.
# Insert the values.
# Commit the changes.
import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
tabela_visual = df_limpo.to_sql("Top_Spotify_Songs", connection, if_exists='replace')

cursor.execute("SELECT * FROM Top_Spotify_Songs")
linha = cursor.fetchall()

for linha in linha:
    print(linha)




# Step 6: Visualize the data (optional, but highly recommended)
# If you haven’t gone through the visualization concepts and practices yet, don’t worry. Try making this work, and we’ll explore visualization in depth in the next few projects.

# What types of visualizations can we make? Suggest at least 3 and plot them.

#Top 20 Songs on Spotify


top_20 = df_limpo.sort_values(by="Streams (billions)", ascending=False).head(20)

plt.figure(figsize = (16, 5))

plt.barh(top_20["Song"][::-1], top_20["Streams (billions)"][::-1])

plt.title("Top 20 Songs on Spotify")
plt.savefig("grafico_top20.png")
plt.show()