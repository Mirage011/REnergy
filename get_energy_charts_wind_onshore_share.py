#python -m pip install requests
import requests
from google.cloud import bigquery
from google.oauth2 import service_account
import json
from datetime import datetime

# Set up BigQuery credentials
credentials = service_account.Credentials.from_service_account_file('access_files\optical-genre-411310-7382265d5700.json')
project_id = 'optical-genre-411310'
dataset_id = 'energytransition'
table_id = 'wind_onshore_daily_avg'

# Set up BigQuery client
client = bigquery.Client(credentials=credentials, project=project_id)

# Make API call
api_url = 'https://api.energy-charts.info/wind_onshore_share_daily_avg?country=de'  # Replace with your API endpoint
response = requests.get(api_url)

# Check if API call was successful
if response.status_code != 200:
    print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
    exit()

# Parse JSON response
try:
    api_data = response.json()
except json.decoder.JSONDecodeError as e:
    print("Error: Failed to parse JSON response from API.")
    exit()

# Check if response contains required fields
if not api_data.get('days') or not api_data.get('data'):
    print("Error: Empty or invalid response received from API.")
    exit()

# Combine 'days' and 'data' into list of tuples with formatted dates
rows_to_insert = [(datetime.strptime(day, '%d.%m.%Y').strftime('%Y-%m-%d'), value) for day, value in zip(api_data['days'], api_data['data'])]


# Define BigQuery schema
schema = [
    bigquery.SchemaField('day', 'DATE'),
    bigquery.SchemaField('value', 'FLOAT')
]
# Create BigQuery table if not exists
table_ref = bigquery.TableReference.from_string(f"{project_id}.{dataset_id}.{table_id}")
table = bigquery.Table(table_ref, schema=schema)
try:
    table = client.create_table(table)
    print(f'Table {table.table_id} created.')
except Exception as e:
    print(f'Table {table.table_id} already exists.')

# Check for existing rows in the table
query = f"SELECT day FROM `{project_id}.{dataset_id}.{table_id}`"
existing_rows = client.query(query).result()

existing_dates = set(row.day for row in existing_rows)

# Filter out rows that already exist in the table
new_rows_to_insert = [(day, value) for day, value in rows_to_insert if day not in existing_dates]


if new_rows_to_insert:
    # Insert new data into BigQuery table
    errors = client.insert_rows(table, new_rows_to_insert)
    if not errors:
        print('New data inserted successfully.')
    else:
        print('Encountered errors while inserting new data.')
        print(errors)
else:
    print('No new data to insert.')
