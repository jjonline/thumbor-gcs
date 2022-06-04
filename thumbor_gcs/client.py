#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.cloud import storage
from google.cloud.storage import Client, Bucket
from thumbor.context import Context


class BucketClient:
    loaderClient: Client = None
    loaderBucket: Bucket = None
    resultClient: Client = None
    resultBucket: Bucket = None
    context: Context = None

    def __init__(self, context):
        """ init GCS when thumbor load thumbor_gcs.loader.gcs_loader"""
        self.context = context
        loader_project_id = context.config.get("LOADER_GCS_PROJECT_ID")
        loader_bucket_id = context.config.get("LOADER_GCS_BUCKET_ID")
        self.loaderClient = storage.Client(loader_project_id)
        self.loaderBucket = self.loaderClient.bucket(loader_bucket_id)

        result_project_id = self.context.config.get("RESULT_STORAGE_GCS_PROJECT_ID")
        result_bucket_id = self.context.config.get("RESULT_STORAGE_GCS_BUCKET_ID")
        """ if loader bucket and result_storage bucket are same, use same instance """
        if result_project_id == loader_project_id and result_bucket_id == loader_bucket_id:
            self.resultClient = self.loaderClient
            self.resultBucket = self.loaderBucket
        else:
            self.resultClient = storage.Client(result_project_id)
            self.resultBucket = self.loaderClient.bucket(result_bucket_id)

    def loader_get_object(self, path: str):
        """Get object from loader bucket.

        :type path: str
        :param path:
            REAL object path in GCS bucket.
            REAL object path is deal from the request PATH of URL.
            for example:
                `https://domain.com/public/sample.png`
                PATH of URL is `/public/sample.png`
                if your config `LOADER_GCS_ROOT_PATH` is EMPTY, then REAL object path is `public/sample.png`
                if your config `LOADER_GCS_ROOT_PATH` is SOME, then REAL object path is `SOME/public/sample.png`
        """
        root_path = self.context.config.LOADER_GCS_ROOT_PATH.strip("/")
        path = f"{root_path}/{path}".lstrip('/')
        return self.loaderBucket.get_blob(path)

    def result_get_object(self, path: str):
        """get object from result bucket.

        :type path: str
        :param path:
            The request path is generated by a certain algorithm, see method normalize_path
        """
        return self.resultBucket.get_blob(path)

    def result_put_object(self, path: str, stream: str or bytes, mime_type: str):
        """put object to result bucket.

        :type path: str
        :param path:
            The request path is generated by a certain algorithm, see method normalize_path

        :type stream: str or bytes
        :param stream:
            file stream str or bytes generate by thumbor core

        :type mime_type: str
        :param mime_type:
            file content-type, determine by thumbor core
        """
        blob = self.resultBucket.blob(path)
        blob.upload_from_string(stream)
        blob.cache_control = "public,max-age=%s" % self.context.config.MAX_AGE
        blob.content_type = mime_type
        blob.patch()
        return path


""" hold global BucketClient instance """
Instance: BucketClient or None = None
