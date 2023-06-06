from .register_commands import setup_register_handlers


def register_all_user_handlers(dp):
    setup_register_handlers(dp)


__all__ = ['register_all_user_handlers']