from django.utils.deconstruct import deconstructible
from storages.backends.ftp import FTPStorage

@deconstructible
class MyFTPStorage(FTPStorage):
    pass