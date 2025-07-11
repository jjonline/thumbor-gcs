from thumbor.loaders import LoaderResult
from thumbor.utils import logger

from thumbor_gcs.storage_manager import get_manager


async def load(context, path):
    """Load an image from GCS."""
    logger.debug("[Loader] loader origin path is %s" % path)

    result = LoaderResult()
    manager = get_manager(context)

    if manager.loader is None:
        logger.error("[Loader] GCS loader not configured")
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
        return result

    blob = manager.loader.get_object(path.lstrip('/'))
    if blob is None:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
    else:
        result.successful = True
        result.buffer = blob.download_as_bytes()
        result.metadata.update(
            size=blob.size,
            updated_at=blob.updated,
        )

    return result
