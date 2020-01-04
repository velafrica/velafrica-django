from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q


class MultiListFilter(admin.ListFilter):
    class Option:
        key = None
        title = None
        query = None

        def __init__(self, key, title, query):
            self.key = key
            self.title = title
            self.query = query

    filters = []
    parameter_name = None

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify a 'parameter_name'."
                % self.__class__.__name__
            )
        if self.parameter_name in params:
            p = params.pop(self.parameter_name)  # needs to be popped
            if p:  # if not empty
                self.filters = p.split('-')

    def options(self) -> [Option]:
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The MultiListFilter.lookups() method must be overridden to '
            'return a list of FilterOptions (key, title, query).'
        )

    def has_output(self):
        return len(self.options()) > 0

    def choices(self, changelist):
        """
        Generates choices for ListFilter bases on the states

        returns choices ready to be output in the template. (self.template = admin/filter.html)
        """
        return [
            {
                "selected": o.key in self.filters,
                "display": o.title,
                "query_string": changelist.get_query_string({
                    # change query string
                    self.parameter_name: "-".join(
                        [x for x in self.filters if x != o.key]  # remove key
                        if o.key in self.filters
                        else self.filters + [o.key]  # add key
                    )
                }) if o.key not in self.filters or len(self.filters) > 1  # if empty
                else changelist.get_query_string(remove=self.parameter_name)  # remove parameter name
            }
            for o in self.options()
        ]

    def expected_parameters(self):
        return [self.parameter_name]

    def queryset(self, request, queryset):
        # adds (logic or) all active queries
        query = Q()
        for o in self.options():
            if o.key in self.filters:
                query |= o.query
        return queryset.filter(query)
