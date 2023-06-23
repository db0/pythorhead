from os.path import basename
from typing import Optional

from pythorhead.requestor import Request, Requestor


class Image:
    def __init__(self, _requestor: Requestor) -> None:
        self._requestor = _requestor

    def upload(self, image_path: str) -> Optional[dict]:
        """

        Upload an image

        Args:
            image_path (str)

        Returns:
            Optional[dict]: image data if successful
        """
        with open(image_path, "rb") as image:
            data = self._requestor.image(
                Request.POST,
                files={"images[]": image},
            )
            if data and "files" in data:
                for file in data["files"]:
                    file["image_url"] = "/".join(
                        (
                            self._requestor._auth.image_url,
                            file["file"],
                        ),
                    )
                    file["delete_url"] = "/".join(
                        (
                            self._requestor._auth.image_url,
                            "delete",
                            file["delete_token"],
                            file["file"],
                        ),
                    )
                    del file["file"]
                    del file["delete_token"]

                return data["files"]
