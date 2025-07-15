import json
import os
import psycopg2
from common.record import Record

def db_writer_handler(event, context):
    """
    Lambda function to write a financial record to the database.

    This function is triggered by an SQS message. It connects to the Aurora
    PostgreSQL database and inserts the record.
    """
    try:
        for sqs_record in event["Records"]:
            record_data = json.loads(sqs_record["body"])
            record = Record.from_dict(record_data)

            conn = psycopg2.connect(
                dbname=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT", 5432)
            )
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO records (record_id, amount, description) VALUES (%s, %s, %s)",
                (record.record_id, record.amount, record.description)
            )

            conn.commit()
            cur.close()
            conn.close()

    except Exception as e:
        # Log the error for debugging and potential reprocessing
        print(f"Error processing SQS message: {e}")
        # Depending on the error, you might want to re-raise it to have SQS
        # retry the message processing.
        raise e
