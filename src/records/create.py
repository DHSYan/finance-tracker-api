import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError

from common.record import Record

def create_record_handler(event, context):
    """
    Lambda function to create a new financial record.

    This function is triggered by an API Gateway POST request. It validates the
    request body, creates a new Record object, and sends it to an SQS queue
    for asynchronous processing by the db_writer Lambda function.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        amount = body.get("amount")
        description = body.get("description")

        # Basic input validation
        if not amount or not description:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Amount and description are required."}),
            }

        # Create a new record with a unique ID
        record = Record(amount=amount, description=description, record_id=str(uuid.uuid4()))

        # Send the record to the SQS queue
        sqs = boto3.client("sqs")
        queue_url = os.environ.get("SQS_QUEUE_URL")
        if not queue_url:
            raise Exception("SQS_QUEUE_URL environment variable not set.")

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(record.to_dict())
        )

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Record created successfully.", "record_id": record.record_id}),
        }

    except (ValueError, TypeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
        }
    except ClientError as e:
        # Log the error for debugging
        print(f"Boto3 client error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not create record due to an internal error."}),
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred."}),
        }
