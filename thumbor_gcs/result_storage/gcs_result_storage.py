#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
from urllib.parse import unquote

from thumbor.result_storages import BaseStorage, ResultStorageResult
from thumbor.utils import logger, deprecated
from thumbor.engines import BaseEngine

import thumbor_gcs.client


class Storage(BaseStorage):

    def __init__(self, context):
        BaseStorage.__init__(self, context)
        """ set instance to global """
        thumbor_gcs.client.Instance = thumbor_gcs.client.BucketClient(context)

    @property
    def is_auto_webp(self):
        return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

    def normalize_path(self, request_path):
        """calculate Path of URL to storage object path.

        :type request_path: str
        :param request_path:
            full PATH of request URL,
            for example:
                URL is `https://domain.com/security/0x0/public/sample.png`
                Then param request_path is `/security/0x0/public/sample.png`
        """
        digest = hashlib.sha1(unquote(request_path).encode("utf-8")).hexdigest()

        """
        To avoid confusion when using the same GCS, you can set RESULT_STORAGE_GCS_ROOT_PATH value
        """
        root_path = thumbor_gcs.client.Instance.result_root_path()
        prefix = "auto_webp" if self.is_auto_webp else "default"

        return f"{root_path}/{prefix}/{digest[:2]}/{digest[2:4]}/{digest[4:]}"

    async def put(self, stream):
        path = self.normalize_path(self.context.request.url)
        try:
            logger.debug("[RESULT_STORAGE] put request URL path is %s" % self.context.request.url)
            logger.debug("[RESULT_STORAGE] put result FILE dir is %s" % path)
            return thumbor_gcs.client.Instance.result_put_object(path, stream, BaseEngine.get_mimetype(stream))
        except Exception as e:
            logger.error(f"[RESULT_STORAGE] put fatal {str(e)} at path {path}")
            return None

    async def get(self):
        """
        value of path example
        /-MvDe9B1kd5wNuDVcuXOqB2PRUs=/0x0/public/article/07902518-0be0-4a60-8789-66d8b31665db.jpeg
        """
        path = self.normalize_path(self.context.request.url)
        try:
            logger.debug("[RESULT_STORAGE] get request URL path is %s" % self.context.request.url)
            logger.debug("[RESULT_STORAGE] get result FILE dir is %s" % path)

            blob = thumbor_gcs.client.Instance.result_get_object(path)
            if blob is None:
                return None

            buffer = blob.download_as_bytes()
            result = ResultStorageResult(
                buffer=buffer,
                metadata={
                    "LastModified": blob.updated,
                    "ContentLength": blob.size,
                    "ContentType": BaseEngine.get_mimetype(buffer),
                },
            )

            return result
        except Exception as e:
            logger.debug(f"[RESULT_STORAGE] get result error {str(e)} at path {path}")
            return None

    @deprecated("Use result's last_modified instead")
    async def last_updated(self):
        path = self.normalize_path(self.context.request.url)
        blob = thumbor_gcs.client.Instance.result_get_object(path)
        if blob is None:
            logger.debug("[RESULT_STORAGE] method last_updated storage not found at %s" % path)
            return True

        return blob.updated
