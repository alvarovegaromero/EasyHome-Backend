from django.contrib import admin

from .forms import ProductToBuyForm
from .models import Product, ProductBought, ProductToBuy


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "group_name", "group_id")

    def group_name(self, obj):
        return obj.group.name

    group_name.short_description = "Group Name"


class ProductToBuyAdmin(admin.ModelAdmin):
    form = ProductToBuyForm
    list_display = ("product_name", "id", "group_name", "group_id")

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product Name"

    def group_id(self, obj):
        return obj.product.group.id

    group_id.short_description = "Group ID"

    def group_name(self, obj):
        return obj.product.group.name

    group_name.short_description = "Group Name"


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductToBuy, ProductToBuyAdmin)
admin.site.register(ProductBought)
