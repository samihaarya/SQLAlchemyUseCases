from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Dict

from gcs_common.exceptions import InvalidRequestException
from sqlalchemy.sql.expression import Select


class FilterOperation(Enum):
    EQUALS = 'EQUALS',
    CONTAINS = 'CONTAINS',
    SORT = 'SORT'


@dataclass
class FilterParam:
    param: str = None
    field: str = None
    value: Union[str, int, bool, list] = None
    operation: FilterOperation = None


class Filter:

    def __init__(self, filter_map: Dict[str, str]):
        self.filter_map: Dict[str, str] = filter_map
        self.filter_params: List[FilterParam] = []

    def add_filter(self, param: str, value, operation: FilterOperation, multi_value: bool = False):
        if value is not None:
            field = self.filter_map.get(param)
            if not field:
                raise InvalidRequestException(f"Invalid filter parameter: {param}")
            if multi_value:
                value = value.split(',')
            self.filter_params.append(FilterParam(
                param=param,
                field=field,
                value=value,
                operation=operation
            ))

    def add_fancy_filters(self, fancy_filter: str):
        if not fancy_filter:
            return
        filter_text: List[str] = fancy_filter.split(' and ')
        for text in filter_text:
            statement_text: List[str] = text.split(' eq ')
            if len(statement_text) != 2:
                raise InvalidRequestException(f'Invalid $filter expression {filter_text}')
            param: str = statement_text[0]
            field: str = self.filter_map.get(param)
            if not field:
                raise InvalidRequestException(f'Invalid $filter field for {filter_text}')
            value = statement_text[1]
            if not value:
                raise InvalidRequestException(f'Missing $filter value for {field}')
            value = value.lstrip("'").rstrip("'")
            self.filter_params.append(FilterParam(
                param=param,
                field=field,
                value=value,
                operation=FilterOperation.EQUALS
            ))

    def add_sort_filters(self, sorts: List[str]):
        if not sorts:
            return
        for sort in sorts:
            s = sort.split(',')
            direction: str = 'ASC'
            if len(s) == 2:
                if s[1] == 'asc':
                    direction = 'ASC'
                elif s[1] == 'desc':
                    direction = 'DESC'
                else:
                    raise InvalidRequestException(f'Invalid sort direction {s[1]}')

            param = s[0]
            field: str = self.filter_map.get(s[0])
            if not field:
                raise InvalidRequestException(f'Invalid sort field for {sort}')

            self.filter_params.append(FilterParam(
                param=param,
                field=field,
                value=direction,
                operation=FilterOperation.SORT
            ))

    def add_ms_style_sort_filters(self, sort_param_value: str):
        if not sort_param_value:
            return
        sorts = sort_param_value.split(',')
        for sort in sorts:
            s = sort.split()
            direction: str = 'ASC'
            if len(s) == 2:
                if s[1] == 'asc':
                    direction = 'ASC'
                elif s[1] == 'desc':
                    direction = 'DESC'
                else:
                    raise InvalidRequestException(f'Invalid sort direction {s[1]}')

            param = s[0]
            field: str = self.filter_map.get(s[0])
            if not field:
                raise InvalidRequestException(f'Invalid sort field for {sort}')

            self.filter_params.append(FilterParam(
                param=param,
                field=field,
                value=direction,
                operation=FilterOperation.SORT
            ))

    def apply_filters(self, statement: Select, table_class: dataclass, default_sort_field) -> Select:
        sort_applied: bool = False
        for fltr in self.filter_params:
            field = getattr(table_class, fltr.field)
            if fltr.operation == FilterOperation.EQUALS:
                statement = statement.where(field == fltr.value)
            elif fltr.operation == FilterOperation.CONTAINS:
                statement = statement.where(field.ilike(f"%{fltr.value}%"))
            elif fltr.operation == FilterOperation.SORT:
                statement = statement.order_by(field.desc() if fltr.value == 'DESC' else field.asc())
                sort_applied = True
        if not sort_applied and default_sort_field:
            # default sort
            statement = statement.order_by(default_sort_field)
        return statement
