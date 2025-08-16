from ui.include.filters import SearchFilterSet


#############################################################################
# Group
#############################################################################


class GroupFilter(SearchFilterSet):
    search_fields = ["name"]


#############################################################################
# User
#############################################################################
class UserFilter(SearchFilterSet):
    search_fields = ["name"]
