from typing import Any, List, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import ListingType, LanguageType


class Site:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def get(
        self,
    ) -> Optional[dict]:
        """
        Get site details.

        Returns:
            dict: site view
        """
        return self._requestor.api(Request.GET, "/site")

    def edit(
        self,
        name: Optional[str] = None,
        sidebar: Optional[str] = None,
        description: Optional[str] = None,
        icon: Optional[str] = None,
        banner: Optional[str] = None,
        enable_downvotes: Optional[bool] = None,
        enable_nsfw: Optional[bool] = None,
        community_creation_admin_only: Optional[bool] = None,
        require_email_verification: Optional[bool] = None,
        application_question: Optional[str] = None,
        private_instance: Optional[bool] = None,
        default_theme: Optional[str] = None,
        default_post_listing_type: Optional[ListingType] = None,
        legal_information: Optional[str] = None,
        application_email_admins: Optional[bool] = None,
        hide_modlog_mod_names: Optional[bool] = None,
        discussion_languages: Optional[List[Union[int, LanguageType]]] = None,
        slur_filter_regex: Optional[str] = None,
        actor_name_max_length: Optional[int] = None,
        rate_limit_message: Optional[int] = None,
        rate_limit_message_per_second: Optional[int] = None,
        rate_limit_post: Optional[int] = None,
        rate_limit_post_per_second: Optional[int] = None,
        rate_limit_register: Optional[int] = None,
        rate_limit_register_per_second: Optional[int] = None,
        rate_limit_image: Optional[int] = None,
        rate_limit_image_per_second: Optional[int] = None,
        rate_limit_comment: Optional[int] = None,
        rate_limit_comment_per_second: Optional[int] = None,
        rate_limit_search: Optional[int] = None,
        rate_limit_search_per_second: Optional[int] = None,
        federation_enabled: Optional[bool] = None,
        federation_debug: Optional[bool] = None,
        federation_worker_count: Optional[int] = None,
        captcha_enabled: Optional[bool] = None,
        captcha_difficulty: Optional[str] = None,
        allowed_instances: Optional[List] = None,
        blocked_instances: Optional[List] = None,
        taglines: Optional[List] = None,
        registration_mode=None,
        reports_email_admins: Optional[bool] = None,
    ) -> Optional[dict]:
        """

        Edit site details

        Args:
            name (str, optional): Defaults to None.
            sidebar (str, optional): Defaults to None.
            description (str, optional): Defaults to None.
            icon (str, optional): Defaults to None.
            banner (str, optional): Defaults to None.
            enable_downvotes (bool, optional): Defaults to None.
            enable_nsfw (bool, optional): Defaults to None.
            community_creation_admin_only (bool, optional): Defaults to None.
            require_email_verification (bool, optional): Defaults to None.
            application_question (str, optional): Defaults to None.
            private_instance (bool, optional): Defaults to None.
            default_theme (str, optional): Defaults to None.
            default_post_listing_type (ListingType, optional): Defaults to None.
            legal_information (str, optional): Defaults to None.
            application_email_admins (bool, optional): Defaults to None.
            hide_modlog_mod_names (bool, optional): Defaults to None.
            discussion_languages: (List[Union[int, LanguageType]], optional): Defaults to None
            slur_filter_regex (str, optional): Defaults to None.
            actor_name_max_length (int, optional): Defaults to None.
            rate_limit_message (int, optional): Defaults to None.
            rate_limit_message_per_second (int, optional): Defaults to None.
            rate_limit_post (int, optional): Defaults to None.
            rate_limit_post_per_second (int, optional): Defaults to None.
            rate_limit_register (int, optional): Defaults to None.
            rate_limit_register_per_second (int, optional): Defaults to None.
            rate_limit_image (int, optional): Defaults to None.
            rate_limit_image_per_second (int, optional): Defaults to None.
            rate_limit_comment (int, optional): Defaults to None.
            rate_limit_comment_per_second (int, optional): Defaults to None.
            rate_limit_search (int, optional): Defaults to None.
            rate_limit_search_per_second (int, optional): Defaults to None.
            federation_enabled (bool, optional): Defaults to None.
            federation_debug (bool, optional): Defaults to None.
            federation_worker_count (int, optional): Defaults to None.
            captcha_enabled (bool, optional): Defaults to None.
            captcha_difficulty (str, optional): Defaults to None.
            allowed_instances (List(str), optional): Defaults to None.
            blocked_instances (List(str), optional): Defaults to None.
            taglines (List(str), optional): Defaults to None.
            registration_mode Defaults to None.
            reports_email_admins (bool, optional): Defaults to None.
        Returns:
            Optional[dict]: post data if successful
        """
        if discussion_languages:
            discussion_languages = [l.value for l in discussion_languages if isinstance(l, LanguageType)]
        edit_site: dict[str, Any] = {
            key: value for key, value in locals().items() if value is not None and key != "self"
        }
        if len(edit_site) == 0:
            raise Exception("Must provide at least one site property to change")

        return self._requestor.api(Request.PUT, "/site", json=edit_site)
