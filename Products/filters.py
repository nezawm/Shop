import django_filters

from Products.models import Product, Category, Brand, ProductSize, Color, ProductVariant


class CategoryFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active"
    )

    class Meta:
        model = Category
        fields = (
            "name",
            "is_active",
        )


class BrandFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Brand
        fields = (
            "name",
        )


class ProductSizeFilter(django_filters.FilterSet):

    size = django_filters.CharFilter(
        field_name="size",
        lookup_expr="icontains"
    )

    class Meta:
        model = ProductSize
        fields = (
            "size",
        )



class ProductVariantFilter(django_filters.FilterSet):

    product = django_filters.CharFilter(
        field_name="product__name",
        lookup_expr="icontains"
    )

    color = django_filters.CharFilter(
        field_name="color__name",
        lookup_expr="icontains"
    )

    size = django_filters.CharFilter(
        field_name="size__size",
        lookup_expr="icontains"
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )

    class Meta:
        model = ProductVariant
        fields = (
            "product",
            "color",
            "size",
            "min_price",
            "max_price",
        )

class ColorFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    color_code = django_filters.CharFilter(
        field_name="color_code",
        lookup_expr="icontains"
    )

    class Meta:
        model = Color
        fields = (
            "name",
            "color_code",
        )

class ProductFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains"
    )

    brand = django_filters.CharFilter(
        field_name="brand__name",
        lookup_expr="icontains"
    )

    gender = django_filters.CharFilter(
        field_name="gender",
        lookup_expr="iexact"
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active"
    )

    class Meta:
        model = Product
        fields = (
            "category",
            "brand",
            "gender",
            "is_active",
        )