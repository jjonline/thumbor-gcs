#!/usr/bin/python
# -*- coding: utf-8 -*-

from thumbor.loaders import LoaderResult
from thumbor.utils import logger

import thumbor_gcs.client


async def load(context, path):
    """
    path is real storage file path
    for example:
        public/article/content/202205/07902518-0be0-4a60-8789-66d8b31665db.jpeg
    """
    logger.debug("[Loader] loader origin path is %s" % path)
    path = path.lstrip('/')

    result = LoaderResult()

    if thumbor_gcs.client.Instance is None:
        thumbor_gcs.client.Instance = thumbor_gcs.client.BucketClient(context)

    blob = thumbor_gcs.client.Instance.loader_get_object(path)
    if blob is None:
        """ file do not exist """
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
    else:
        """ file exist """
        result.successful = True
        result.buffer = blob.download_as_bytes()

        result.metadata.update(
            size=blob.size,
            updated_at=blob.updated,
        )

    return result
