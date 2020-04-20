import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime as dt

class S3Interface():
    """
    S3Interface class is the key to load your modules or objects
    from S3 to the code. This class's functionality is enabled
    using s3_client and s3_resource class variables. These would be shared among
    multiple objects.
    """
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    def __init__(self, bucket_name):
        """
        Set the bucket name using the constructor
        """
        self.bucket_name = bucket_name

    def get_all_buckets(self):
        """
        Fetches all the bucket names which are present in the account
        """
        return [b.name for b in self.s3_resource.buckets.all()]


    def get_file(self, file_name):
        """
        Returns the file. Do note that the expectation here is that the
        file which is being returned is a json.
        """
        data = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
        contents = data['Body'].read().decode('utf-8')
        return json.loads(contents)

    def upload_file(self, raw_file, bucket_name, object_name, type):
        """
        Uploads a given file into a bucket under a given key (S3 file name)
        :param raw_file: Raw file to be uploaded
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. This expects the account number of the uploader
        """
        try:
            raw_file.seek(0)
            # Appending prefix and suffix
            prefix = 'export/'+type+'/'
            object_name = prefix + object_name + get_current_date()
            # resp = self.s3_client.upload_file(file_name, bucket_name, object_name)
            self.s3_client.put_object(Bucket=bucket_name, Body=raw_file.getvalue(), Key=object_name)
        except ClientError as e:
            print(e)
            return False
        return True    


def get_current_date():
    """
    Utility function for tagging uploaded files with current date
    """
    now = dt.now()
    date = now.strftime("/%d/%m/%y/%H-%M-%S")
    return date