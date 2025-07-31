from typing import Optional

from google.cloud import storage
from thumbor.context import Context
from thumbor.utils import logger

from thumbor_gcs.client import StorageClient

_gcs_clients = {}


def get_storage_client(project_id: Optional[str] = None) -> storage.Client:
    """
    Get or create a raw storage.Client instance for the given project_id.
    If project_id is None, the default project from the environment is used.
    """
    if project_id not in _gcs_clients:
        project_desc = f"'{project_id}'" if project_id else "default project"
        logger.debug(f"GCS Client for {project_desc} not found. Creating new storage client")
        _gcs_clients[project_id] = storage.Client(project_id) if project_id else storage.Client()

    return _gcs_clients[project_id]


class StorageManager:
    def __init__(self, context: Context):
        self.context = context
        self._loader: Optional[StorageClient] = None
        self._result: Optional[StorageClient] = None

    @property
    def loader(self) -> Optional[StorageClient]:
        """Get a loader client, creating it if necessary."""

        if not hasattr(self.context.config, 'LOADER_GCS_BUCKET_ID'):
            return None

        if self._loader is None and self.context.config.LOADER_GCS_BUCKET_ID:
            project_id = getattr(self.context.config, 'LOADER_GCS_PROJECT_ID', None)
            bucket_id = self.context.config.LOADER_GCS_BUCKET_ID
            root_path = getattr(self.context.config, 'LOADER_GCS_ROOT_PATH', '')
            self._loader = StorageClient(
                gcs_client=get_storage_client(project_id),
                bucket_id=bucket_id,
                root_path=root_path
            )
        return self._loader

    @property
    def result(self) -> Optional[StorageClient]:
        """Get a result storage client, creating it if necessary."""

        if not hasattr(self.context.config, 'RESULT_STORAGE_GCS_BUCKET_ID'):
            return None

        if self._result is None and self.context.config.RESULT_STORAGE_GCS_BUCKET_ID:
            project_id = getattr(self.context.config, 'RESULT_STORAGE_GCS_PROJECT_ID', None)
            bucket_id = self.context.config.RESULT_STORAGE_GCS_BUCKET_ID
            root_path = getattr(self.context.config, 'RESULT_STORAGE_GCS_ROOT_PATH', '')
            self._result = StorageClient(
                gcs_client=get_storage_client(project_id),
                bucket_id=bucket_id,
                root_path=root_path
            )
        return self._result
