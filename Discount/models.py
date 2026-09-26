from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from Core.base_models import SoftDeleteModel


class Discount(SoftDeleteModel):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    percentage = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=True
    )

    is_first_purchase = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expired_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(days=3)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'


class DiscountUsage(models.Model):

    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='usages'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discount_usages'
    )

    order = models.OneToOneField(
        'Order.Order',
        on_delete=models.CASCADE,
        related_name='discount_usage'
    )

    used_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        verbose_name = 'Discount Usage'
        verbose_name_plural = 'Discount Usages'

        constraints = [

            models.UniqueConstraint(
                fields=[
                    'discount',
                    'user'
                ],
                name='unique_discount_per_user'
            )

        ]

    def __str__(self):

        return f'{self.user} - {self.discount.code}'