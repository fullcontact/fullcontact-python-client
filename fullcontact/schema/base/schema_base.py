# -*- coding: utf-8 -*-

"""
This module serves the base class for validating
FullContact API requests.
"""

import collections.abc
from abc import ABCMeta, abstractmethod
from typing import get_type_hints, Iterable, Union

from ...exceptions import FullContactException


class BaseRequestSchema(object, metaclass=ABCMeta):
    required_fields = ()
    queryable_fields = ()

    @property
    @abstractmethod
    def schema_name(self) -> str:
        pass

    @staticmethod
    def _check_iter_item(attr_type: type,
                         iter_data: Union[list, tuple, Iterable]
                         ) -> Union[list, tuple, Iterable]:
        r"""
        Validate items in an iterator.

        :param attr_type: Type of the iterative attribute (List/Tuple/Iterable).
        :param iter_data: iterable data
        :return: validated iterable data
        """
        iter_type = attr_type.__args__[0]
        if isinstance(iter_type(), BaseRequestSchema):
            return [
                iter_type().validate(data_item)
                for data_item in iter_data
            ]
        for iter_item in iter_data:
            if not isinstance(iter_item, iter_type):
                raise FullContactException(
                    'Argument %r is not of type %s in %s' % (
                        iter_item, iter_type, str(iter_data)
                    )
                )

        return iter_data

    def _is_queryable(self, validated_data: dict) -> bool:
        r"""
        Check if the minimum queryable items are present or not.

        :param validated_data: dict data that has been validated.
        :return: True if at least 1 queryable item is present
        """
        if len(self.queryable_fields) == 0 or len(
                set.intersection(
                    set(self.queryable_fields), set(validated_data.keys())
                )
        ) > 0:
            return True
        return False

    def _raise_required_fields_exception(self):
        r"""
        Raise FullContactException if required fields are not provided.
        """
        connector = "are" if len(self.required_fields) > 1 else "is"
        raise FullContactException(
            "For %s query, %s %s required." % (
                self.schema_name, ','.join(self.required_fields), connector
            )
        )

    def validate(self, data: dict) -> dict:
        r"""
        Validate the dict data against the type hints.

        :param data: dict data to be validated.
        :return: validated data. FullContactException will be raised for invalid
        type.
        """
        valid_fields = {}
        type_hints = get_type_hints(self.__class__)

        # iterate all type hints
        for attr_name, attr_type in type_hints.items():
            if attr_name == 'return':
                continue

            # Ignore empty field if it is not a required field.
            elif attr_name not in self.required_fields and data.get(
                    attr_name, None) is None:
                continue

            # Raise exception if a required field is empty.
            elif data.get(attr_name, None) is None:
                self._raise_required_fields_exception()

            # If the type is iterable, iterate over every item and validate.
            elif hasattr(attr_type, "__origin__") and attr_type.__origin__ in \
                    (list, tuple, collections.abc.Iterable):
                valid_fields[attr_name] = self._check_iter_item(
                    attr_type,
                    data[attr_name]
                )

            # If the item is an instance of a schema, call its validate method.
            elif isinstance(attr_type(), BaseRequestSchema):
                valid_fields[attr_name] = attr_type().validate(data[attr_name])

            # Raise for type mismatch.
            elif not isinstance(data[attr_name], attr_type):
                raise FullContactException(
                    'Query item %r in %s has to be of type %s' % (attr_name, self.schema_name, attr_type)
                )

            # Add successfully validated field to valid_fields.
            else:
                valid_fields[attr_name] = data[attr_name]

        if not self._is_queryable(valid_fields):
            raise FullContactException(
                "No queryable inputs given (for example: %s)" % (', '.join(self.queryable_fields))
            )
        return valid_fields


class BaseCombinationRequestSchema(BaseRequestSchema):
    @property
    @abstractmethod
    def field_combinations(self) -> Iterable[tuple]:
        r"""
        Allowed field combinations for the query type.

        :return: an iterable with tuples of valid combinations
        FullContactException will be raised if an invalid combination is provided
        """
        pass

    def _raise_invalid_combination_exception(self):
        r"""
        Raise FullContactException mentioning possible combinations.
        """
        combinations_strings = [" + ".join(field_combination)
                                for field_combination in
                                sorted(
                                    self.field_combinations, key=len,
                                    reverse=True
                                )]
        error_message = "\n".join(combinations_strings)
        raise FullContactException(
            "Possible combinations to query by %s are:\n%s" % (
                self.schema_name, error_message)
        )

    def validate(self, data: dict) -> dict:
        r"""
        Validate the field types and combinations.

        :param data: dict data to be validated.
        :return: validated data.
        Type validation will be done using the base class, allowed
        combinations will be validated using field_combinations.
        """
        valid_fields = {}
        type_validated_data = super().validate(data)

        for field_combination in sorted(self.field_combinations, key=len,
                                        reverse=True):
            if len(set(field_combination) - set(type_validated_data.keys())) == 0:
                valid_fields = type_validated_data
                break

        if len(valid_fields.items()) == 0:
            self._raise_invalid_combination_exception()

        return valid_fields
