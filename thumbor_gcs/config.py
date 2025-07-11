from thumbor.config import Config

Config.define(
    "LOADER_GCS_PROJECT_ID",
    "",
    "project id for google cloud storage used for loader.",
    "GCS Storage",
)

Config.define(
    "LOADER_GCS_BUCKET_ID",
    "",
    "bucket id for google cloud storage used for loader.",
    "GCS Storage",
)

Config.define(
    "RESULT_STORAGE_GCS_PROJECT_ID",
    "",
    "project id for google cloud storage used for result storage.",
    "GCS Storage",
)

Config.define(
    "RESULT_STORAGE_GCS_BUCKET_ID",
    "",
    "bucket id for google cloud storage used for result storage.",
    "GCS Storage",
)

Config.define(
    "LOADER_GCS_ROOT_PATH",
    "",
    "set google cloud storage object prefix path used for loader.",
    "GCS Storage",
)

Config.define(
    "RESULT_STORAGE_GCS_ROOT_PATH",
    "",
    "set google cloud storage object prefix path used for result storage.",
    "GCS Storage",
)
