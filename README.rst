thumbor-gcs
===========

Thumbor Loader and Result Storage for `Google Cloud
Storage <https://cloud.google.com/storage>`__ ,it can also be
abbreviated as ``gcs``

   📢 Attention

   The thumbor storage can be customized as follows:
   `Storages <https://thumbor.readthedocs.io/en/latest/custom_storages.html>`__,
   `Image
   Loaders <https://thumbor.readthedocs.io/en/latest/custom_loaders.html>`__,
   `Result
   Storages <https://thumbor.readthedocs.io/en/latest/custom_result_storages.html>`__.

   This project currently only implements ``Image Loaders`` and
   ``Result Storages``

Installation
============

::

   pip install thumbor-gcs

Authentication
==============

Authentication is handled by the Google Cloud Storage SDK, see
``google-cloud-storage`` SDK
`documentation <https://googleapis.dev/python/storage/latest/index.html>`__

Contribution
============

You can make a pull requests
`HERE <https://github.com/jjonline/thumbor-gcs/pulls>`__, thank you for
your contribution.

Configuration
=============

You should create the corresponding bucket first in google cloud storage

Loader settings
---------------

::

   LOADER = 'thumbor_gcs.loader.gcs_loader'
   # set your google cloud storage bucket name
   LOADER_GCS_BUCKET_ID = ''
   # set your google cloud project id
   LOADER_GCS_PROJECT_ID = ''
   LOADER_GCS_ROOT_PATH = ''

..

   Assuming ``LOADER_GCS_ROOT_PATH`` is set to ``original``, if the PATH
   of the URL is ``/public/sample.png``, then the file storage path in
   the bucket of google cloud storage is ``original/public/sample.png``

Result storage settings
-----------------------

::

   RESULT_STORAGE = 'thumbor_gcs.result_storage.gcs_result_storage'
   # set your google cloud storage bucket name
   RESULT_STORAGE_GCS_BUCKET_ID = ''
   # set your google cloud project id
   RESULT_STORAGE_GCS_PROJECT_ID = ''
   RESULT_STORAGE_GCS_ROOT_PATH = ''

Other
=====

   If your ``Image Loaders`` and ``Result Storages`` use the same
   bucket, please use the two configuration items
   ``LOADER_GCS_ROOT_PATH`` and ``RESULT_STORAGE_GCS_ROOT_PATH`` as
   appropriate, and pay attention to the file storage path (also called
   ``object path``) in this bucket.
