from django.contrib import admin
from django.utils import timezone


class SoftDeleteAdmin(admin.ModelAdmin):

    actions = (
        "soft_delete_selected",
        "restore_selected",
        "hard_delete_selected",
    )

    list_filter = (
        "is_deleted",
    )

    readonly_fields = (
        "is_deleted",
        "deleted_at",
    )

    @admin.display(
        boolean=True,
        description="Deleted"
    )
    def deleted(self, obj):
        return obj.is_deleted

    def get_queryset(self, request):
        return self.model.all_objects.all()

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()

    @admin.action(description="Soft Delete selected")
    def soft_delete_selected(self, request, queryset):
        queryset.delete()

    @admin.action(description="Restore selected")
    def restore_selected(self, request, queryset):

        queryset.update(
            is_deleted=False,
            deleted_at=None
        )

    @admin.action(description="Hard Delete selected")
    def hard_delete_selected(self, request, queryset):
        queryset.hard_delete()

    def get_actions(self, request):

        actions = super().get_actions(request)

        actions.pop("delete_selected", None)

        return actions