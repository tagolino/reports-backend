from django.db.models import Manager


class CustomerPortalManager(Manager):
    def get_queryset(self):
        return super().get_queryset().using("customer_portal")
