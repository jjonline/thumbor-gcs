from typing import Optional, Dict

from google.cloud import storage
from thumbor.context import Context

from thumbor_gcs.client import GCSClient


class StorageManager:
    def __init__(self, context: Context):
        self.context = context
        self._loader: Optional[GCSClient] = None
        self._result: Optional[GCSClient] = None
        self._gcs_clients: Dict[str, storage.Client] = {}

    def _get_or_create_gcs_client(self, project_id: str) -> storage.Client:
        """Get an existing GCS client or create a new one for the given project."""
        if project_id not in self._gcs_clients:
            self._gcs_clients[project_id] = storage.Client(project_id)
        return self._gcs_clients[project_id]

    @property
    def loader(self) -> Optional[GCSClient]:
        """Get a loader client, creating it if necessary."""
        if not hasattr(self.context.config, 'LOADER_GCS_PROJECT_ID'):
            return None

        if self._loader is None and self.context.config.LOADER_GCS_PROJECT_ID:
            gcs_client = self._get_or_create_gcs_client(self.context.config.LOADER_GCS_PROJECT_ID)
            self._loader = GCSClient(
                gcs_client=gcs_client,
                bucket_id=self.context.config.LOADER_GCS_BUCKET_ID,
                root_path=getattr(self.context.config, 'LOADER_GCS_ROOT_PATH', '')
            )
        return self._loader

    @property
    def result(self) -> Optional[GCSClient]:
        """Get a result storage client, creating it if necessary."""
        if not hasattr(self.context.config, 'RESULT_STORAGE_GCS_PROJECT_ID'):
            return None

        if self._result is None and self.context.config.RESULT_STORAGE_GCS_PROJECT_ID:
            gcs_client = self._get_or_create_gcs_client(self.context.config.RESULT_STORAGE_GCS_PROJECT_ID)
            self._result = GCSClient(
                gcs_client=gcs_client,
                bucket_id=self.context.config.RESULT_STORAGE_GCS_BUCKET_ID,
                root_path=getattr(self.context.config, 'RESULT_STORAGE_GCS_ROOT_PATH', '')
            )
        return self._result


# Global instance but per-context
_managers = {}


def get_manager(context: Context) -> StorageManager:
    """Get or create a StorageManager instance for the given context."""
    if context not in _managers:
        _managers[context] = StorageManager(context)
    return _managers[context]
