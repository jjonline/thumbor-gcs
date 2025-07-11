import hashlib
from urllib.parse import unquote

from thumbor.engines import BaseEngine
from thumbor.result_storages import BaseStorage, ResultStorageResult
from thumbor.utils import logger, deprecated

from thumbor_gcs.storage_manager import get_manager


class Storage(BaseStorage):
    def __init__(self, context):
        BaseStorage.__init__(self, context)
        self.manager = get_manager(context)

    @property
    def is_auto_webp(self):
        return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

    def normalize_path(self, request_path):
        digest = hashlib.sha1(unquote(request_path).encode("utf-8")).hexdigest()
        prefix = "auto_webp" if self.is_auto_webp else "default"
        return f"{prefix}/{digest[:2]}/{digest[2:4]}/{digest[4:]}"

    async def put(self, stream):
        if self.manager.result is None:
            logger.error("[RESULT_STORAGE] GCS result storage not configured")
            return None

        path = self.normalize_path(self.context.request.url)
        try:
            logger.debug("[RESULT_STORAGE] put request URL path is %s" % self.context.request.url)
            logger.debug("[RESULT_STORAGE] put result FILE dir is %s" % path)
            return self.manager.result.put_object(
                path=path,
                stream=stream,
                mime_type=BaseEngine.get_mimetype(stream),
                max_age=self.context.config.MAX_AGE
            )
        except Exception as e:
            logger.error(f"[RESULT_STORAGE] put fatal {str(e)} at path {path}")
            return None

    async def get(self):
        if self.manager.result is None:
            return None

        path = self.normalize_path(self.context.request.url)
        try:
            logger.debug("[RESULT_STORAGE] get request URL path is %s" % self.context.request.url)
            logger.debug("[RESULT_STORAGE] get result FILE dir is %s" % path)

            blob = self.manager.result.get_object(path)
            if blob is None:
                return None

            buffer = blob.download_as_bytes()
            return ResultStorageResult(
                buffer=buffer,
                metadata={
                    "LastModified": blob.updated,
                    "ContentLength": blob.size,
                    "ContentType": BaseEngine.get_mimetype(buffer),
                },
            )
        except Exception as e:
            logger.debug(f"[RESULT_STORAGE] get result error {str(e)} at path {path}")
            return None

    @deprecated("Use result's last_modified instead")
    async def last_updated(self):
        if self.manager.result is None:
            return True

        path = self.normalize_path(self.context.request.url)
        blob = self.manager.result.get_object(path)
        if blob is None:
            logger.debug("[RESULT_STORAGE] method last_updated storage not found at %s" % path)
            return True
        return blob.updated
