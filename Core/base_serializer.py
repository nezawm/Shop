from rest_framework import serializers

from Core.fields import JalaliDateTimeField


class BaseSerializer(serializers.ModelSerializer):
    """
    اگر مدل created_at یا updated_at داشته باشد،
    خروجی آنها به صورت شمسی نمایش داده می‌شود.
    """

    def get_fields(self):

        fields = super().get_fields()

        model = self.Meta.model

        model_fields = {
            field.name
            for field in model._meta.get_fields()
        }

        if "created_at" in model_fields:

            fields["created_at"] = JalaliDateTimeField(
                read_only=True
            )

        if "updated_at" in model_fields:

            fields["updated_at"] = JalaliDateTimeField(
                read_only=True
            )

        return fields