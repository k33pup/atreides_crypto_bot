from .license_commands import setup_license_handlers


def register_all_admin_handlers(dp):
    setup_license_handlers(dp)


__all__ = ['register_all_admin_handlers']