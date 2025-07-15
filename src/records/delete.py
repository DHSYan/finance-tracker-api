import json
import os
import psycopg2

def delete_record_handler(event, context):
    """
    Lambda function to delete a financial record from the database.

    This function is triggered by an API Gateway DELETE request. It connects to the
    Aurora PostgreSQL database and deletes the record.
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

        cur.execute("DELETE FROM records WHERE record_id = %s", (record_id,))

        conn.commit()
        deleted_rows = cur.rowcount
        cur.close()
        conn.close()

        if deleted_rows > 0:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Record deleted successfully."})
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Record not found."})
            }

    except Exception as e:
        print(f"Error deleting record: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred."})
        }
