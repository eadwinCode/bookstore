import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.stores.models import StoreBook

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StoreBook)
def notify_available_books_subscribers(sender, **kwargs):
    store_book: StoreBook = kwargs['instance']
    if store_book.is_available and not store_book.borrowed_by:
        pass
