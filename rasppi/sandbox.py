import boto3
import time
from config import region_name, aws_access_key_id, aws_secret_access_key, queue_name

sqs = boto3.resource('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
queue = sqs.get_queue_by_name(QueueName=queue_name)

def main():
    while True:
        for message in queue.receive_messages():
            print(message.body)
            message.delete()
            time.sleep(10)
    

if __name__ == "__main__":
    main()