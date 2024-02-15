from django.db.models import Manager


class DataServiceManager(Manager):
    def get_queryset(self):
        return super().get_queryset().using("data_service")
