from .models import SocialLink, Announcement, ContactInfo, ContactMessage
from django.utils import timezone


def global_context(request):
    social_links = SocialLink.objects.all()
    contact_info = ContactInfo.objects.first()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    # Active announcement
    now = timezone.now()
    announcement = Announcement.objects.filter(
        is_active=True,
        start_date__lte=now
    ).filter(
        end_date__isnull=True
    ).first() or Announcement.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).first()

    return {
        'social_links': social_links,
        'contact_info': contact_info,
        'active_announcement': announcement,
        'unread_messages_count': unread_messages,
    }
