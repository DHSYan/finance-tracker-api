import json
import os
import psycopg2

def get_record_handler(event, context):
    """
    Lambda function to retrieve a financial record from the database.

    This function is triggered by an API Gateway GET request. It connects to the
    Aurora PostgreSQL database and retrieves the record.
    """
    try:
        record_id = event["pathParameters"]["record_id"]

        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT", 5432)
        )
        cur = conn.cursor()

        cur.execute("SELECT record_id, amount, description FROM records WHERE record_id = %s", (record_id,))
        record = cur.fetchone()

        cur.close()
        conn.close()

        if record:
            return {
                "statusCode": 200,
                "body": json.dumps({"record_id": record[0], "amount": record[1], "description": record[2]})
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Record not found."})
            }

    except Exception as e:
        print(f"Error retrieving record: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred."})
        }
