import math
from dataclasses import dataclass
from typing import Generic, List, TypeVar, Callable

from sqlalchemy import select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import Select, func, SelectBase

T = TypeVar('T')


@dataclass
class Page(Generic[T]):
    """
    Represents a set of set of paged data.  It can be used loaded with data (elements) and total_pages and
    total_elements after a query or used to define the page and size with which to make a paged query.
    """
    elements: List[dict] = None
    page: int = 0
    size: int = 10
    total_elements: int = None
    total_pages: int = None

    def calculate_pagination_totals(self, select_stmt: SelectBase, session: Session):
        """
        Calculates and sets the total elements and pages for the given sql statement.  Page.size must be set
        to the same limit that was used in the corresponding paged query

        Parameters
        ----------
        select_stmt: SelectBase
            The Select or TextualSelect that was used to run the
            paged SQL query that we want get a totals count for.  Can be either a select() or text() sql statement but
            it must be before the limit and offset were applied. (For TextualSelect this means you'll need a different
            statement than the limited one for getting an individual page)
        session: Session
            Session for the current transaction to execute the count query
        """
        count_stmt: Select = select(func.count()).select_from(select_stmt.options().subquery())
        result = session.execute(count_stmt)
        self.total_elements = result.scalar_one_or_none()
        self.total_pages = math.ceil(self.total_elements / self.size)

    def make_paged(self, select_stmt: Select) -> Select:
        """
        Adds paging limit and offset to the given select sql statement based on this Page objects size and page
        Parameters
        ----------
        select_stmt: Select

        Returns
        -------
        Select
            The given select with the paged limit (page) and offset (page * size) applied
        """
        return select_stmt.limit(self.size).offset(self.page * self.size)

    def to_dict(self, element_converter: Callable[[T], dict]) -> dict:
        """
        Converts the Page to a dictionary.  Useful for json serialization
        Parameters
        ----------
        element_converter: Callable[[T], dict]
            A callable (ex: function or lambda) that will convert an element object to a dictionary. If the element
            type is already a dict then just return the callables input

        Returns
        -------
        dict
            Dictionary representation of the page
        """

        page: dict = {
            "elements": self.elements,
            # "elements": [element_converter(e) for e in self.elements],
            "totalNumberOfElements": self.total_elements,
            "totalNumberOfPages": self.total_pages
        }

        return page
