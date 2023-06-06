from .is_client import ClientFilter
from .is_admin import AdminFilter


def register_all_filters(dp):
    dp.filters_factory.bind(ClientFilter)
    dp.filters_factory.bind(AdminFilter)


__all__ = ['register_all_filters']