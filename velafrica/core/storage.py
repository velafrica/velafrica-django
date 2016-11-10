# -*- coding: utf-8 -*-
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage

@deconstructible
class MyStorage(S3Boto3Storage):
    """
    TODO: write doc
    """
    pass