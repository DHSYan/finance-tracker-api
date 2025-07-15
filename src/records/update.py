import json
import os
import psycopg2

def update_record_handler(event, context):
    """
    Lambda function to update a financial record in the database.

    This function is triggered by an API Gateway PUT request. It connects to the
    Aurora PostgreSQL database and updates the record.
    """
    try:
        record_id = event["pathParameters"]["record_id"]
        body = json.loads(event.get("body", "{}"))
        amount = body.get("amount")
        description = body.get("description")

        if not amount and not description:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Amount or description must be provided for update."})
            }

        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT", 5432)
        )
        cur = conn.cursor()

        if amount and description:
            cur.execute("UPDATE records SET amount = %s, description = %s WHERE record_id = %s", (amount, description, record_id))
        elif amount:
            cur.execute("UPDATE records SET amount = %s WHERE record_id = %s", (amount, record_id))
        else:
            cur.execute("UPDATE records SET description = %s WHERE record_id = %s", (description, record_id))

        conn.commit()
        updated_rows = cur.rowcount
        cur.close()
        conn.close()

        if updated_rows > 0:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Record updated successfully."})
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Record not found."})
            }

    except Exception as e:
        print(f"Error updating record: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred."})
        }
