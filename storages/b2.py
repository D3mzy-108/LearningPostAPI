from django.core.files.storage import Storage
from django.conf import settings
from b2sdk.v2 import InMemoryAccountInfo, B2Api
import os


class BackblazeB2Storage(Storage):
    def __init__(self):
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account(
            "production", settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.bucket = self.b2_api.get_bucket_by_name(
            settings.AWS_STORAGE_BUCKET_NAME)

    def _save(self, name, content):
        name = self._clean_name(name)
        content.open()
        file_data = content.read()
        self.bucket.upload_bytes(file_data, name)
        content.close()
        return name

    def _open(self, name, mode='rb'):
        # This can be implemented if you want to retrieve the file
        pass

    def url(self, name):
        name = self._clean_name(name)
        return f"https://f003.backblazeb2.com/file/{settings.AWS_STORAGE_BUCKET_NAME}/media/{name}"

    def exists(self, name):
        name = self._clean_name(name)
        file_versions = self.bucket.list_file_versions(file_name=name)
        return any(file_version.file_name == name for file_version in file_versions)

    def _clean_name(self, name):
        return os.path.normpath(name).replace('\\', '/')
