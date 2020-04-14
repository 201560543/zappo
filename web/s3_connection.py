import json
import boto3

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

