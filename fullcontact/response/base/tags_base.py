# -*- coding: utf-8 -*-

"""
This module serves the base class for wrapping
FullContact Tags API response.
"""

from collections import defaultdict
from typing import List, Dict

from .base import BaseApiResponse


class BaseTagsResponse(BaseApiResponse):

    def _tags_to_lists_dict(self, tags: List[Dict]):
        tags = tags or {}

        transformed_tags = defaultdict(list)
        for tag in tags:
            transformed_tags[tag.get("key")] \
                .append(tag.get("value"))

        return dict(transformed_tags)

    def get_tags(self):
        return self._tags_to_lists_dict(
            self.json().get("tags", None) or {}
        )
