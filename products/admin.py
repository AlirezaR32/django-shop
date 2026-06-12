from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Product, Category, Brand, Image, OffCode


# ── Inlines ──────────────────────────────────────────────────────────────────

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ("image", "img_number")
    readonly_fields = ("img_number",)
    ordering = ("img_number",)


# ── Product ───────────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    list_display = (
        "title",
        "brand",
        "category",
        "price",
        "off_percent",
        "final_price",
        "stock_quantity",
        "review_avg_point",
        "sell_count",
        "view_count",
        "is_active",
        "created_at",
    )
    list_filter = ( "is_active", "brand", "category")
    search_fields = ("title", "short_desc", "brand__name", "category__name")
    list_editable = ( "is_active",)
    readonly_fields = ("final_price", "review_avg_point", "review_count",
                       "view_count", "sell_count", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "short_desc", "desc", "brand", "category"),
        }),
        ("Pricing", {
            "fields": ("price", "off_percent", "final_price"),
        }),
        ("Inventory", {
            "fields": ("stock_quantity","is_active"),
        }),
        ("Stats", {
            "fields": ("review_avg_point", "review_count", "view_count", "sell_count"),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    @admin.display(description="Available", boolean=True)
    def is_available(self, obj):
        return obj.is_available

# ── Category ─────────────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("name",)


# ── Brand ─────────────────────────────────────────────────────────────────────

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_preview", "logo")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px; object-fit:contain;" />',
                obj.logo,
            )
        return "—"


# ── Image ─────────────────────────────────────────────────────────────────────

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("product", "img_number", "image")
    list_filter = ("product",)
    search_fields = ("product__title",)
    readonly_fields = ("img_number",)
    ordering = ("product", "img_number")


# ── OffCode ───────────────────────────────────────────────────────────────────

@admin.register(OffCode)
class OffCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "off_percent", "status_badge")
    search_fields = ("code",)

    @admin.display(description="Status")
    def status_badge(self, obj):
        if obj.exipred_at > timezone.now():
            return format_html(
                '<span style="color:white; background:#2e7d32; padding:2px 8px;'
                ' border-radius:4px; font-size:11px;">Active</span>'
            )
        return format_html(
            '<span style="color:white; background:#c62828; padding:2px 8px;'
            ' border-radius:4px; font-size:11px;">Expired</span>'
        )
