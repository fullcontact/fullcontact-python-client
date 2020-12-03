# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Audience Create and Download
API Responses.
"""

from typing import BinaryIO, Union

from .base.base import BaseApiResponse


class AudienceCreateResponse(BaseApiResponse):
    def get_requestId(self):
        return self.json().get("requestId", None)


class AudienceDownloadResponse(BaseApiResponse):
    # Being a .json.gzip file download, only a status 200 is successful
    SUCCESSFUL_STATUS_CODES = (200,)

    def _copy_fileobj_in_chunks(self, source_file: BinaryIO, dest_file: BinaryIO):
        for chunk in source_file:
            dest_file.write(chunk)

    def write_to_file(self, file: Union[str, BinaryIO]):
        r"""
        Write the downloaded file contents to a file object or file path.

        :param file: The file path or file object to write
        """
        if self.is_successful:
            if isinstance(file, str):
                with open(file, "wb") as download_file:
                    self._copy_fileobj_in_chunks(self.response, download_file)
                    return True

            elif hasattr(file, "write"):
                self._copy_fileobj_in_chunks(self.response, file)
                return True

        return False
