# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact Tags API request classes.
"""

from abc import ABCMeta
from typing import Dict, List

from .base_api import BaseApi


class TagsBaseApi(BaseApi, metaclass=ABCMeta):

    def _tags_dict_to_list(self, tags: Dict) -> List[Dict]:
        r"""
        Convert tags dictionary to a list of dictionaries.

        :param tags: Dictionary of tags

        :return: Tags converted to list of dictionaries.

        Example Input:
        {
            "tag1": "I am a sample tag"
            "tag2": ["Another sample tag", "yet another sample tag"]
        }

        The output for the above input will be as follows:
        [
            {
                "key": "tag1",
                "value": "I am a sample tag"
            },
            {
                "key": "tag2",
                "value": "Another sample tag"
            },
            {
                "key": "tag2",
                "value": "yet another sample tag"
            }
        ]
        """
        tags_list = []

        for tag_key, tag_values in tags.items():
            if type(tag_values) != list:
                tag_values = [tag_values]

            for tag_value in tag_values:
                tags_list.append(dict(key=tag_key, value=tag_value))

        return tags_list
