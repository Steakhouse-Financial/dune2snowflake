import pandas as pd
import snowflake
import traceback
from snowflake import connector
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query
import hashlib
import os, sys, requests
import argparse
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
from email.mime.text import MIMEText

def pull_data_from_dune(query_id,date_to_pull):
    # Function that pulls data from Dune query
    query = Query(
    name="@pipistrella / Lido Protocol Economics (Daily) with eth value/trp",
    query_id=query_id,
    params=[
        QueryParameter.date_type(name="date_from", value=date_to_pull),
    ],
)
    #print("Results available at", query.url())

    dune = DuneClient(os.environ.get("DUNE_API_KEY"))
    data = dune.refresh_into_dataframe(query)
    data = data.replace({'<nil>':0})
    data.to_csv('dune_results.csv', header=True, index = False)
    return data


def upsert_to_snowflake(df,id_columns,insert_columns,update_columns,table,stage):
	# Function that inserts data to Snowflake from results of Dune query
	if df.empty: 
		print(f'No rows to bulk upsert to {table}. Aborting.')
		return

	with snowflake.connector.connect(
		user = os.environ.get("SNOWFLAKE_USER"), 
		password = os.environ.get("SNOWFLAKE_PASSWORD"),
		account = os.environ.get("SNOWFLAKE_ACCOUNT"),
		warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE"), # name of a fitting warehouse
		database = os.environ.get("SNOWFLAKE_DATABASE"),
		schema = os.environ.get("SNOWFLAKE_SCHEMA"),
	) as con:

		cur = con.cursor()

		print(f"BULK UPSERTING {df.shape[0]} {table.upper()} TO SNOWFLAKE")

		# convert to json
		filename = f"{table}.json"
		df.to_json(filename,orient='records',lines=True,date_unit='s')
		filepath = os.path.abspath(filename)

		# it can be a good idea to systematically convert to UTC
		# timestamps will be uploaded to your default timezone if you don't
		cur.execute("alter session set timezone='UTC';")
		cur.execute(f"put file://{filepath} @{stage} overwrite=true;")
		cur.execute(f"""merge into {table}
						using (select {','.join([f'$1:{col} as {col}' for col in insert_columns])}
							from @{stage}/{filename}) t
						on ({' and '.join([f't.{col} = {table}.{col}' for col in id_columns])})
						when matched then
							update set {','.join([f'{col}=t.{col}' for col in update_columns])}
						when not matched then insert ({','.join(insert_columns)})
						values ({','.join([f't.{col}' for col in insert_columns])});""")
		# delete json file from the table stage
		cur.execute(f"remove @{stage}/{filename};")
		# delete the json file created
		os.remove(filename)
		print('\tData upsert into Snowflake completed.')

		cur.close()
		
# Function to hash each row of the DataFrame
def hash_row(row):
    # Concatenate all values in the row as a string
    row_str = ''.join(str(x) for x in row)
    # Calculate the SHA256 hash of the row string
    hash_obj = hashlib.sha256(row_str.encode())
    return hash_obj.hexdigest()        

def send_email(subject, body, recipients):
    # Send email via gmail SMTP
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.environ.get("SMTP_SENDER")
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(os.environ.get("SMTP_SENDER"), os.environ.get("SMTP_PASSWORD"))
    smtp_server.sendmail(os.environ.get("SMTP_SENDER"), recipients, msg.as_string())
    smtp_server.quit() 

## Start of __main__
if __name__ == "__main__":
    recipients = ["hi@charkoal.xyz", "a@smolco.xyz"]
    
    try:
        #sys.exit(0)
        print("Executing script:{} at {}".format(sys.argv[0], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # Create an ArgumentParser object
        parser = argparse.ArgumentParser(description='Pull data from Dune and write to Snowflake')

        # Add command line arguments
        parser.add_argument('--days', type=int, help='No of days of data to pull from Dune')

        # Parse the command line arguments
        args = parser.parse_args()

        # Derive date to pull data from Dune
        if args.days:
            date_to_pull = datetime.today() - timedelta(days=args.days)
        else: #default is 1 day pull
            date_to_pull = datetime.today() - timedelta(days=1)
        date_to_pull = date_to_pull.strftime("%Y-%m-%d") + " 00:00:00"
        print("Data pull from Dune starting {}".format(date_to_pull))    

        # Define parameters needed
        table_name = os.environ.get("TABLE_NAME")
        stage_name = os.environ.get("STAGE_NAME")
        query_id = os.environ.get("DUNE_QUERY_ID")

        # Pull data from Dune
        df_dune_Data = pull_data_from_dune(query_id,date_to_pull)
        # Comment above and uncomment below for quick testing
        #df_dune_Data = pd.read_csv('dune_results.csv')
        # Convert columns to uppercase
        df_dune_Data.columns = map(lambda x: str(x).upper(), df_dune_Data.columns)
        # Include hash column
        df_dune_Data['HASH_KEY'] = df_dune_Data.apply(hash_row, axis=1)
        print("Columns inserted to Snowflake are {}".format(df_dune_Data.columns))
        print("No of records from Dune is {}".format(df_dune_Data.shape[0]))
        # Remove duplicates if exists
        df_dune_Data['PERIOD'] = df_dune_Data['PERIOD'].astype('str')
        df_dune_Data = df_dune_Data.drop_duplicates(subset='HASH_KEY', keep="first", inplace=False)
        print("No of records from after removing duplicates is {}".format(df_dune_Data.shape[0]))
        df_dune_Data.to_csv('dune_results_hash.csv', header=True, index = False)
        print(df_dune_Data.dtypes)
        # Prepare for Snowflake upsert
        id_columns = ['HASH_KEY']
        insert_columns = df_dune_Data.columns
        update_columns = insert_columns.remove('HASH_KEY')
        # Run Snowflake upsert logic
        upsert_to_snowflake(df_dune_Data,id_columns,insert_columns,update_columns,table_name,stage_name)
        print("** Data pull from Dune and upsert to Snowflake completed.")
        print("** Script execution completed at {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        subject = "Dune 2 Snowflake execution Completed"
        send_email(subject,"Data loaded from Dune to Snowflake successfully for date range >= {} and inserted {} records".format(date_to_pull,df_dune_Data.shape[0]),recipients)
        # Uptime push notification
        requests.get(os.environ.get("UPTIME_URL"))

    except Exception as e:
        subject = "Error in Dune to Snowflake execution"
        send_email(subject,str(''.join(traceback.TracebackException.from_exception(e).format())),recipients)


