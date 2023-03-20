from system.db_routing.middleware import get_current_db_name


class SystemRouter:

    @staticmethod
    def db_for_read(self, model, **hints):
        return get_current_db_name()

    @staticmethod
    def db_for_write(self, model, **hints):
        return get_current_db_name()

    @staticmethod
    def allow_relation(self, *args, **kwargs):
        return True

    @staticmethod
    def allow_syncdb(self, *args, **kwargs):
        return None

    @staticmethod
    def allow_migrate(self, *args, **kwargs):
        return None

