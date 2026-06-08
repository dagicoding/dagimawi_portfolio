from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    HomeProfile, Role, Skill, Statistic, SocialLink,
    PortfolioCategory, PortfolioWork, PortfolioImage,
    Testimonial, ContactInfo, ContactMessage, Announcement,
    Service, Experience
)


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 3
    fields = ('image', 'caption', 'order')


@admin.register(HomeProfile)
class HomeProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at')
    fieldsets = (
        ('Identity', {'fields': ('name', 'profile_image', 'description')}),
        ('Files', {'fields': ('cv_file',)}),
    )

    def has_add_permission(self, request):
        return not HomeProfile.objects.exists()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'icon', 'order')
    list_editable = ('percentage', 'order')


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('value', 'order')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order')
    list_editable = ('order',)


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PortfolioWork)
class PortfolioWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'is_visible', 'created_at', 'thumbnail_preview')
    list_filter = ('category', 'featured', 'is_visible')
    list_editable = ('featured', 'is_visible')
    search_fields = ('title', 'description')
    inlines = [PortfolioImageInline]
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'description', 'category')}),
        ('Media', {'fields': ('cover_image', 'video_file', 'video_url')}),
        ('Settings', {'fields': ('featured', 'is_visible', 'created_at', 'order')}),
    )

    def thumbnail_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.cover_image.url)
        return "—"
    thumbnail_preview.short_description = "Preview"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'rating', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'is_archived')
    list_filter = ('is_read', 'is_archived')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    actions = ['mark_read', 'mark_unread', 'archive']

    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = "Mark selected as read"

    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_unread.short_description = "Mark selected as unread"

    def archive(self, request, queryset):
        queryset.update(is_archived=True)
    archive.short_description = "Archive selected"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active', 'start_date', 'end_date')
    list_editable = ('is_active',)
    list_filter = ('type', 'is_active')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'is_current', 'order')
    list_editable = ('order',)
