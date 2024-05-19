# Import necessary libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests
import psycopg2
import os

def get_html(url):
    """
    Fetches the HTML content of the given URL.
    """
    response = requests.get(url)
    return response.text

def extract_events(html):
    """
    Extracts event data from the HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')
    events = []

    for event in soup.find_all('li', class_='event-item fl-clr yellow'):
        date = event.find_all('div', class_='cell xlarge-6 body-small')

        data = date[0].text.strip().split('|')

        title = event.find('p', class_='event-title h3').text.strip()
        data.append(title)

        artists = date[1].text.strip().replace('Program', '').replace(' ', '').replace('\n', '').replace('.', '').split('|')
        data.append(artists)

        works = event.find('div', class_='body-small').text.strip()
        data.append(works)

        img_link = event.find('source').get('srcset')
        img = 'https://www.lucernefestival.ch' + img_link
        data.append(img)

        events.append(data)
    
    return events

def clean_data(events):
    """
    Cleans and structures the extracted event data.
    """
    df = pd.DataFrame(events, columns=['Date', 'Time', 'Location', 'Title', 'Artists', 'Event', 'Link'])
    df['Date'] = pd.to_datetime(df['Date'].apply(lambda x: x[-7:-1] + '24'), format= '%d.%m.%y', dayfirst=True)
    df['Time'] = df['Time'].apply(lambda x: x[1:3] + ":" + x[4:6])
    df['Artists'] = df['Artists'].apply(lambda x: ', '.join(x))
    df['Artists'] = df['Artists'].replace('', 'NA')
    df.index = range(1, len(df) + 1)
    df['id'] = df.index
    df = df[['id', 'Date', 'Time', 'Location', 'Title', 'Artists', 'Event', 'Link']]
    
    return df

def load_to_db(df):
    """
    Loads the cleaned data into the PostgreSQL database.
    """
    # Database connection parameters from environment variables
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'port': '5432'
    }

    drop_table_query = 'DROP TABLE IF EXISTS sample_data'

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS sample_data (
        id INT PRIMARY KEY,
        Day DATE,
        Time TIME,
        Location VARCHAR(100),
        Title VARCHAR(500),
        Artists VARCHAR(500),
        Event VARCHAR(100),
        Link VARCHAR(500)
    )
    '''

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)
    conn.commit()

    insert_query = '''
    INSERT INTO sample_data (id, Day, Time, Location, Title, Artists, Event, Link)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    '''

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    url = 'https://www.lucernefestival.ch/en/program/summer-festival-24'
    html = get_html(url)
    events = extract_events(html)
    df = clean_data(events)
    load_to_db(df)

if __name__ == "__main__":
    main()
