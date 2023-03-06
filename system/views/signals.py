from system.models.loans import Loan
from system.models.cashflows import CashFlow
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.cache import cache, caches


@receiver(pre_save, sender=CashFlow)
@receiver(pre_save, sender=Loan)
def invalidate_cache(sender, *args, **kwargs):
    cache.delete("statistics")

# @receiver(pre_save, sender=CashFlow)
# @receiver(pre_save, sender=Loan)
# def invalidate_cache(sender, *args, **kwargs):
#     caches["statistics"].delete()
