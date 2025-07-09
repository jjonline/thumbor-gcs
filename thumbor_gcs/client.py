from google.cloud import storage


class GCSClient:
    def __init__(self, gcs_client: storage.Client, bucket_id: str, root_path: str = ''):
        """Initialize GCS client wrapper.

        Args:
            gcs_client: Google Cloud Storage client instance
            bucket_id: ID of the GCS bucket
            root_path: Optional root path prefix for all operations
        """
        self.client = gcs_client
        self.bucket = self.client.bucket(bucket_id)
        self.root_path = root_path.rstrip("/")

    def get_object(self, path: str):
        """Get an object from a GCS bucket.

        Args:
            path: Object path in GCS bucket
        """

        if self.root_path:
            path = f"{self.root_path}/{path}"

        return self.bucket.get_blob(path)

    def put_object(self, path: str, stream: str or bytes, mime_type: str, max_age: int = None):
        """Put an object to the GCS bucket.

        Args:
            path: Object path in GCS bucket
            stream: File content as string or bytes
            mime_type: Content type of the file
            max_age: Cache control max age in seconds
        """
        blob = self.bucket.blob(path)
        blob.upload_from_string(stream)
        if max_age is not None:
            blob.cache_control = f"public,max-age={max_age}"
        blob.content_type = mime_type
        blob.patch()
        return path
