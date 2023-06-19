from typing import Optional, List

from pythorhead.types import ListingType, CommentSortType
from pythorhead.requestor import Requestor, Request


class Comment:
    def __init__(self):
        self._requestor = Requestor()

    def list(
        self,
        community_id: Optional[int] = None,
        community_name: Optional[str] = None,
        limit: Optional[int] = None,
        max_depth: Optional[int] = None,
        page: Optional[int] = None,
        parent_id: Optional[int] = None,
        post_id: Optional[int] = None,
        saved_only: Optional[bool] = None,
        sort: Optional[CommentSortType] = None,
        type_: Optional[ListingType] = None,
    ) -> List[dict]:
        """
        
        Get comments, with various filters.

        Args:
            community_id (Optional[int], optional): Defaults to None.
            community_name (Optional[str], optional): Defaults to None.
            limit (Optional[int], optional): Defaults to None.
            max_depth (Optional[int], optional): Defaults to None.
            page (Optional[int], optional): Defaults to None.
            parent_id (Optional[int], optional): Defaults to None.
            post_id (Optional[int], optional): Defaults to None.
            saved_only (Optional[bool], optional): Defaults to None.
            sort (Optional[CommentSortType], optional): Defaults to None.
            type_ (Optional[ListingType], optional): Defaults to None.

        Returns:
            List[dict]: list of comments
        """
        list_comment = {}
        if community_id is not None:
            list_comment["community_id"] = community_id
        if community_name is not None:
            list_comment["community_name"] = community_name
        if limit is not None:
            list_comment["limit"] = limit
        if max_depth is not None:
            list_comment["max_depth"] = max_depth
        if page is not None:
            list_comment["page"] = page
        if parent_id is not None:
            list_comment["parent_id"] = parent_id
        if post_id is not None:
            list_comment["post_id"] = post_id
        if saved_only is not None:
            list_comment["saved_only"] = saved_only
        if sort is not None:
            list_comment["sort"] = sort
        if type_ is not None:
            list_comment["type"] = type_

        if data := self._requestor.request(Request.GET, "/comment/list", params=list_comment):
            return data["comments"]
        return []

        
    def create(
        self,
        post_id: int,
        content: str,
        form_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        language_id: Optional[int] = None,
    ) -> Optional[dict]:
        """
        Create a comment.

        Args:
            post_id (int): post_id
            content (str): content
            form_id (Optional[int], optional): Defaults to None.
            parent_id (Optional[int], optional): Defaults to None.
            language_id (Optional[int], optional): Defaults to None.
        
        Returns:
            dict: created comment data if successful
        """

        create_comment = {
            "post_id": post_id,
            "content": content,
        }
        if form_id is not None:
            create_comment["form_id"] = form_id
        if parent_id is not None:
            create_comment["parent_id"] = parent_id
        if language_id is not None:
            create_comment["language_id"] = language_id

        return self._requestor.request(
            Request.POST,
            "/comment",
            json=create_comment,
        )

    __call__ = create