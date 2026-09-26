from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.base_models import SoftDeleteModel

# Create your models here.
class Category(SoftDeleteModel):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}  Activity is -->{self.is_active}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')



class ProductSize(SoftDeleteModel):
    SIZE_TYPE_CHOICES = (
        ('S', _('Small')),
        ('M', _('Medium')),
        ('L', _('Large')),
        ('XL', _('Extra Large')),
        ('XXL', _('Extra Extra Large')),
    )
    size=models.CharField(max_length=10, verbose_name=_('Size'), choices=SIZE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f'{self.size} Size'
    class Meta:
        verbose_name = _('Product Size')
        verbose_name_plural = _('Product Sizes')

class Brand(SoftDeleteModel):
    name=models.CharField(max_length=50, verbose_name=_('Name'))
    logo=models.ImageField(verbose_name=_('Logo'), upload_to='brands/', null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')




from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.base_models import SoftDeleteModel


class Product(SoftDeleteModel):

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNISEX = 'U', _('Unisex')

    name = models.CharField(max_length=50, verbose_name=_('Name'), null=True, blank=True)
    target_gender = models.CharField(max_length=1, choices=Gender, default=Gender.UNISEX, verbose_name=_('Target Gender'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('Category'), null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name=_('Brand'), null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Discount'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))


    def __str__(self):
        return self.name or f'Product #{self.pk}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']


class ProductImage(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='images', verbose_name=_('Product'), null=True, blank=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to='products/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')



class Color(SoftDeleteModel):
    name = models.CharField(max_length=50, verbose_name=_('Name'), null=True, blank=True)
    color_code=models.CharField(max_length=50, verbose_name=_('Color Code'), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f'{self.name} code is ---> {self.color_code}'

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')


class ProductVariant(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='variants', verbose_name=_('Product'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='products/', null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, verbose_name=_('Size'))
    color= models.ForeignKey(Color, on_delete=models.PROTECT, verbose_name=_('Color'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    stock=models.PositiveIntegerField(default=0, verbose_name=_('Stock'))
    discount=models.DecimalField(max_digits=10, decimal_places=2, default=0 ,verbose_name=_('Discount'))
    is_active=models.BooleanField(default=True, verbose_name=_('Is Active'))

    def __str__(self):
        return f'{self.product.name} ---> {self.size}'

    class Meta:
        verbose_name = _('ProductVariant')
        verbose_name_plural = _('ProductVariants')



