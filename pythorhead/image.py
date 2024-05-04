from os.path import basename
from PIL import Image as PillowImage
from pythorhead.requestor import Request, Requestor
from io import BytesIO


class Image:
    def __init__(self, _requestor: Requestor) -> None:
        self._requestor = _requestor

    def upload(self, image):
        """

        Upload an image

        Args:
            image (str, PIL.Image): Image ins str or PIL format

        Returns:
            Optional[dict]: pictrs upload data, if successful
        """
        data = None
        if isinstance(image, str):            
            with open(image, "rb") as image_bytes:
                data = self._requestor.image(
                    Request.POST,
                    files={"images[]": image_bytes},
                )
        else:
                img: PillowImage = image
                img_byte_array = BytesIO()
                image_bytes = img.save(img_byte_array, format='webp', quality=95)
                img_byte_array.seek(0)

                data = self._requestor.image(
                    Request.POST,
                    files={"images[]": img_byte_array},
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
        
    def delete(self, image_delete_url: str):
        """

        Delete an lemmy image via pictrs

        Args:
            image_delete_url (str): The pictrs delete URL

        Returns:
            bool: True is succesfully deleted
        """
        req = self._requestor.image_del(
            Request.GET,
            image_delete_url,
        )
        return req.ok
