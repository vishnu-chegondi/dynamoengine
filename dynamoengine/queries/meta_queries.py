import boto3
import os


class Cursor():

    def __init__(self):
        if os.getenv('ENDPOINT_URL'):
            self.client = boto3.client(
                'dynamodb',
                endpoint_url=os.getenv('ENDPOINT_URL'),
                region_name='us-east-1'
                )
        else:
            self.client = boto3.client('dynamodb', region_name='us-east-1')


if __name__ == "__main__":
    os.environ['ENDPOINT_URL'] = 'http://localhost:8800'
    cursor = Cursor()
    print(cursor.client.list_tables())
