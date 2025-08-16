"""Filter definitions for Group and User models.

These filters are used in list views and API endpoints to provide
search functionality.
"""

from ui.include.filters import SearchFilterSet


#############################################################################
# Group
#############################################################################


class GroupFilter(SearchFilterSet):
    """Filter class for the `Group` model.

    Enables searching by group name.
    """

    search_fields = ["name"]


#############################################################################
# User
#############################################################################


class UserFilter(SearchFilterSet):
    """Filter class for the `User` model.

    Enables searching by user name.
    """

    search_fields = ["name"]
