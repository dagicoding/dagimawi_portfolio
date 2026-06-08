from django.db import models
from django.utils import timezone


class HomeProfile(models.Model):
    name = models.CharField(max_length=200, default="Dagimawi Tarekegne")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    description = models.TextField(blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Profile"
        verbose_name_plural = "Home Profile"

    def __str__(self):
        return self.name


class Role(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(default=80)
    icon = models.CharField(max_length=100, blank=True, help_text="CSS class e.g. bi bi-brush")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Statistic(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=20, help_text="e.g. 50+")
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('telegram', 'Telegram'),
        ('linkedin', 'LinkedIn'),
        ('behance', 'Behance'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=100, blank=True, help_text="Bootstrap icon class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.platform


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Portfolio Categories"

    def __str__(self):
        return self.name


class PortfolioWork(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(PortfolioCategory, on_delete=models.SET_NULL, null=True, related_name='works')
    cover_image = models.ImageField(upload_to='works/')
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at', 'order']

    def __str__(self):
        return self.title


class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(PortfolioWork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='works/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.portfolio.title}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    company = models.CharField(max_length=100, blank=True)
    rating = models.PositiveIntegerField(default=5)
    review = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.company}"


class ContactInfo(models.Model):
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return "Contact Information"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Announcement(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('promo', 'Promotion'),
    ]
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.URLField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_currently_active(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.end_date and now > self.end_date:
            return False
        return now >= self.start_date


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"
