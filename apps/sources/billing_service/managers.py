from django.db.models import Manager


class BillingServiceManager(Manager):
    def get_queryset(self):
        return super().get_queryset().using("billing_service")
