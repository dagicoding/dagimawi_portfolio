from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages as django_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .models import (
    HomeProfile, Role, Skill, Statistic, SocialLink,
    PortfolioCategory, PortfolioWork, PortfolioImage, Testimonial,
    ContactInfo, ContactMessage, Announcement, Service, Experience
)
from .forms import ContactForm


# ─────────────────────────────────────────────
# PUBLIC PAGES
# ─────────────────────────────────────────────

def home(request):
    profile = HomeProfile.objects.first()
    roles = Role.objects.all()
    skills = Skill.objects.all()
    stats = Statistic.objects.all()
    featured_works = PortfolioWork.objects.filter(featured=True, is_visible=True).select_related('category')[:6]
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'portfolio/home.html', {
        'profile': profile, 'roles': roles, 'skills': skills,
        'stats': stats, 'featured_works': featured_works,
        'testimonials': testimonials, 'page_title': 'Home',
    })


def works(request):
    categories = PortfolioCategory.objects.all()
    works_qs = PortfolioWork.objects.filter(is_visible=True).select_related('category')
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(PortfolioCategory, slug=category_slug)
        works_qs = works_qs.filter(category=selected_category)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [{'id': w.id, 'title': w.title,
                 'category': w.category.name if w.category else '',
                 'category_slug': w.category.slug if w.category else '',
                 'cover_image': w.cover_image.url if w.cover_image else '',
                 'url': f'/works/{w.id}/'} for w in works_qs]
        return JsonResponse({'works': data})

    return render(request, 'portfolio/works.html', {
        'works': works_qs, 'categories': categories,
        'selected_category': selected_category, 'page_title': 'Works',
    })


def work_detail(request, pk):
    work = get_object_or_404(PortfolioWork, pk=pk, is_visible=True)
    gallery = work.images.all()
    related = PortfolioWork.objects.filter(category=work.category, is_visible=True).exclude(pk=pk)[:4]
    return render(request, 'portfolio/work_detail.html', {
        'work': work, 'gallery': gallery, 'related': related, 'page_title': work.title,
    })


def category_works(request, slug):
    category = get_object_or_404(PortfolioCategory, slug=slug)
    works_qs = PortfolioWork.objects.filter(category=category, is_visible=True)
    return render(request, 'portfolio/category_works.html', {
        'category': category, 'works': works_qs, 'page_title': category.name,
    })


def poster_design(request):
    try:
        category = PortfolioCategory.objects.get(slug='poster-design')
        works_qs = PortfolioWork.objects.filter(category=category, is_visible=True)
    except PortfolioCategory.DoesNotExist:
        works_qs = PortfolioWork.objects.none(); category = None
    return render(request, 'portfolio/category_page.html', {
        'works': works_qs, 'category': category, 'page_title': 'Poster Design',
        'hero_title': 'Poster Design', 'hero_subtitle': 'Creative visual storytelling through stunning poster designs',
    })


def thumbnail_design(request):
    try:
        category = PortfolioCategory.objects.get(slug='thumbnail-design')
        works_qs = PortfolioWork.objects.filter(category=category, is_visible=True)
    except PortfolioCategory.DoesNotExist:
        works_qs = PortfolioWork.objects.none(); category = None
    return render(request, 'portfolio/category_page.html', {
        'works': works_qs, 'category': category, 'page_title': 'Thumbnail Design',
        'hero_title': 'Thumbnail Design', 'hero_subtitle': 'Eye-catching thumbnails that boost clicks and engagement',
    })


def logo_design(request):
    try:
        category = PortfolioCategory.objects.get(slug='logo-design')
        works_qs = PortfolioWork.objects.filter(category=category, is_visible=True)
    except PortfolioCategory.DoesNotExist:
        works_qs = PortfolioWork.objects.none(); category = None
    return render(request, 'portfolio/category_page.html', {
        'works': works_qs, 'category': category, 'page_title': 'Logo Design',
        'hero_title': 'Logo Design', 'hero_subtitle': 'Iconic logos that define brands and make lasting impressions',
    })


def video_editing(request):
    try:
        category = PortfolioCategory.objects.get(slug='video-editing')
        works_qs = PortfolioWork.objects.filter(category=category, is_visible=True)
    except PortfolioCategory.DoesNotExist:
        works_qs = PortfolioWork.objects.none(); category = None
    return render(request, 'portfolio/video_page.html', {
        'works': works_qs, 'category': category, 'page_title': 'Video Editing',
        'hero_title': 'Video Editing', 'hero_subtitle': 'Cinematic edits that captivate audiences and tell powerful stories',
    })


def about(request):
    profile = HomeProfile.objects.first()
    skills = Skill.objects.all()
    services = Service.objects.all()
    experiences = Experience.objects.all()
    stats = Statistic.objects.all()
    return render(request, 'portfolio/about.html', {
        'profile': profile, 'skills': skills, 'services': services,
        'experiences': experiences, 'stats': stats, 'page_title': 'About',
    })


def contact(request):
    contact_info = ContactInfo.objects.first()
    social_links = SocialLink.objects.all()
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Send email notification
            _send_contact_email(msg, contact_info)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
            django_messages.success(request, 'Your message has been sent successfully!')
            return redirect('portfolio:contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'portfolio/contact.html', {
        'form': form, 'contact_info': contact_info,
        'social_links': social_links, 'page_title': 'Contact',
    })


def _send_contact_email(msg, contact_info):
    """Send email notification when a new contact message is received."""
    recipient = contact_info.email if contact_info and contact_info.email else None
    if not recipient:
        return
    try:
        send_mail(
            subject=f'[Portfolio] New Message: {msg.subject}',
            message=(
                f'You received a new message from your portfolio website.\n\n'
                f'──────────────────────────\n'
                f'From:    {msg.name}\n'
                f'Email:   {msg.email}\n'
                f'Subject: {msg.subject}\n'
                f'──────────────────────────\n\n'
                f'{msg.message}\n\n'
                f'──────────────────────────\n'
                f'Reply directly to: {msg.email}\n'
                f'Received at: {msg.created_at.strftime("%Y-%m-%d %H:%M UTC")}\n'
            ),
            from_email=getattr(django_settings, 'DEFAULT_FROM_EMAIL', 'portfolio@dagimawi.com'),
            recipient_list=[recipient],
            fail_silently=True,
        )
    except Exception:
        pass  # Never crash the user's submission due to email failure


def download_cv(request):
    profile = HomeProfile.objects.first()
    if profile and profile.cv_file:
        response = HttpResponse(profile.cv_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Dagimawi_Tarekegne_CV.pdf"'
        return response
    return redirect('portfolio:home')


# ─────────────────────────────────────────────
# CUSTOM DASHBOARD AUTH
# ─────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('portfolio:dashboard_home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('portfolio:dashboard_home')
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials or insufficient permissions.'})
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('portfolio:dashboard_login')


# ─────────────────────────────────────────────
# DASHBOARD VIEWS (staff only)
# ─────────────────────────────────────────────

@login_required(login_url='/dashboard/login/')
def dashboard_home(request):
    if not request.user.is_staff:
        return redirect('portfolio:home')
    ctx = {
        'total_works': PortfolioWork.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_skills': Skill.objects.count(),
        'total_announcements': Announcement.objects.filter(is_active=True).count(),
        'recent_messages': ContactMessage.objects.filter(is_archived=False)[:5],
        'recent_works': PortfolioWork.objects.order_by('-created_at')[:5],
        'featured_count': PortfolioWork.objects.filter(featured=True).count(),
    }
    return render(request, 'dashboard/home.html', ctx)


# ── PROFILE ──
@login_required(login_url='/dashboard/login/')
def dashboard_profile(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    profile = HomeProfile.objects.first()
    roles = Role.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_profile':
            if not profile:
                profile = HomeProfile()
            profile.name = request.POST.get('name', profile.name if profile else '')
            profile.description = request.POST.get('description', '')
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            if 'cv_file' in request.FILES:
                profile.cv_file = request.FILES['cv_file']
            profile.save()
            django_messages.success(request, 'Profile updated successfully.')
        elif action == 'add_role':
            title = request.POST.get('role_title', '').strip()
            if title:
                Role.objects.create(title=title, order=Role.objects.count())
                django_messages.success(request, f'Role "{title}" added.')
        elif action == 'delete_role':
            role_id = request.POST.get('role_id')
            Role.objects.filter(id=role_id).delete()
            django_messages.success(request, 'Role deleted.')
        return redirect('portfolio:dashboard_profile')
    return render(request, 'dashboard/profile.html', {'profile': profile, 'roles': roles})


# ── WORKS ──
@login_required(login_url='/dashboard/login/')
def dashboard_works(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    works_qs = PortfolioWork.objects.select_related('category').order_by('-created_at')
    categories = PortfolioCategory.objects.all()
    return render(request, 'dashboard/works.html', {'works': works_qs, 'categories': categories})


@login_required(login_url='/dashboard/login/')
def dashboard_work_add(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    categories = PortfolioCategory.objects.all()
    if request.method == 'POST':
        cat_id = request.POST.get('category')
        work = PortfolioWork(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            video_url=request.POST.get('video_url', ''),
            featured=request.POST.get('featured') == 'on',
            is_visible=request.POST.get('is_visible', 'on') == 'on',
        )
        if cat_id:
            work.category_id = cat_id
        if 'cover_image' in request.FILES:
            work.cover_image = request.FILES['cover_image']
        if 'video_file' in request.FILES:
            work.video_file = request.FILES['video_file']
        work.save()
        for img in request.FILES.getlist('gallery_images'):
            PortfolioImage.objects.create(portfolio=work, image=img)
        django_messages.success(request, f'Work "{work.title}" added.')
        return redirect('portfolio:dashboard_works')
    return render(request, 'dashboard/work_form.html', {'categories': categories, 'mode': 'add'})


@login_required(login_url='/dashboard/login/')
def dashboard_work_edit(request, pk):
    if not request.user.is_staff: return redirect('portfolio:home')
    work = get_object_or_404(PortfolioWork, pk=pk)
    categories = PortfolioCategory.objects.all()
    if request.method == 'POST':
        work.title = request.POST.get('title', work.title)
        work.description = request.POST.get('description', '')
        work.video_url = request.POST.get('video_url', '')
        work.featured = request.POST.get('featured') == 'on'
        work.is_visible = request.POST.get('is_visible', 'on') == 'on'
        cat_id = request.POST.get('category')
        work.category_id = cat_id if cat_id else None
        if 'cover_image' in request.FILES:
            work.cover_image = request.FILES['cover_image']
        if 'video_file' in request.FILES:
            work.video_file = request.FILES['video_file']
        work.save()
        for img in request.FILES.getlist('gallery_images'):
            PortfolioImage.objects.create(portfolio=work, image=img)
        django_messages.success(request, f'Work "{work.title}" updated.')
        return redirect('portfolio:dashboard_works')
    return render(request, 'dashboard/work_form.html', {'work': work, 'categories': categories, 'mode': 'edit'})


@login_required(login_url='/dashboard/login/')
def dashboard_work_delete(request, pk):
    if not request.user.is_staff: return redirect('portfolio:home')
    work = get_object_or_404(PortfolioWork, pk=pk)
    name = work.title
    work.delete()
    django_messages.success(request, f'Work "{name}" deleted.')
    return redirect('portfolio:dashboard_works')


@login_required(login_url='/dashboard/login/')
def dashboard_work_toggle(request, pk):
    if not request.user.is_staff: return redirect('portfolio:home')
    work = get_object_or_404(PortfolioWork, pk=pk)
    field = request.POST.get('field')
    if field == 'featured':
        work.featured = not work.featured
    elif field == 'visible':
        work.is_visible = not work.is_visible
    work.save()
    return JsonResponse({'ok': True})


# ── MESSAGES ──
@login_required(login_url='/dashboard/login/')
def dashboard_messages(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    filter_by = request.GET.get('filter', 'all')
    msgs = ContactMessage.objects.all()
    if filter_by == 'unread':
        msgs = msgs.filter(is_read=False, is_archived=False)
    elif filter_by == 'archived':
        msgs = msgs.filter(is_archived=True)
    else:
        msgs = msgs.filter(is_archived=False)
    return render(request, 'dashboard/messages.html', {'messages_list': msgs, 'filter': filter_by})


@login_required(login_url='/dashboard/login/')
def dashboard_message_detail(request, pk):
    if not request.user.is_staff: return redirect('portfolio:home')
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'dashboard/message_detail.html', {'msg': msg})


@login_required(login_url='/dashboard/login/')
def dashboard_message_action(request, pk):
    if not request.user.is_staff: return redirect('portfolio:home')
    msg = get_object_or_404(ContactMessage, pk=pk)
    action = request.POST.get('action')
    if action == 'archive':
        msg.is_archived = True; msg.save()
        django_messages.success(request, 'Message archived.')
    elif action == 'unarchive':
        msg.is_archived = False; msg.save()
        django_messages.success(request, 'Message restored.')
    elif action == 'mark_read':
        msg.is_read = True; msg.save()
    elif action == 'delete':
        msg.delete()
        django_messages.success(request, 'Message deleted.')
        return redirect('portfolio:dashboard_messages')
    return redirect('portfolio:dashboard_message_detail', pk=pk)


# ── SKILLS ──
@login_required(login_url='/dashboard/login/')
def dashboard_skills(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Skill.objects.create(
                name=request.POST.get('name', ''),
                percentage=int(request.POST.get('percentage', 80)),
                icon=request.POST.get('icon', ''),
                order=Skill.objects.count(),
            )
            django_messages.success(request, 'Skill added.')
        elif action == 'edit':
            skill = get_object_or_404(Skill, pk=request.POST.get('id'))
            skill.name = request.POST.get('name', skill.name)
            skill.percentage = int(request.POST.get('percentage', skill.percentage))
            skill.icon = request.POST.get('icon', skill.icon)
            skill.save()
            django_messages.success(request, 'Skill updated.')
        elif action == 'delete':
            Skill.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Skill deleted.')
        return redirect('portfolio:dashboard_skills')
    return render(request, 'dashboard/skills.html', {'skills': Skill.objects.all()})


# ── TESTIMONIALS ──
@login_required(login_url='/dashboard/login/')
def dashboard_testimonials(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            t = Testimonial(
                client_name=request.POST.get('client_name', ''),
                company=request.POST.get('company', ''),
                rating=int(request.POST.get('rating', 5)),
                review=request.POST.get('review', ''),
                is_active=request.POST.get('is_active') == 'on',
                order=Testimonial.objects.count(),
            )
            if 'client_image' in request.FILES:
                t.client_image = request.FILES['client_image']
            t.save()
            django_messages.success(request, 'Testimonial added.')
        elif action == 'delete':
            Testimonial.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Testimonial deleted.')
        elif action == 'toggle':
            t = get_object_or_404(Testimonial, pk=request.POST.get('id'))
            t.is_active = not t.is_active; t.save()
        return redirect('portfolio:dashboard_testimonials')
    return render(request, 'dashboard/testimonials.html', {'testimonials': Testimonial.objects.all()})


# ── ANNOUNCEMENTS ──
@login_required(login_url='/dashboard/login/')
def dashboard_announcements(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Announcement.objects.create(
                title=request.POST.get('title', ''),
                message=request.POST.get('message', ''),
                type=request.POST.get('type', 'info'),
                button_text=request.POST.get('button_text', ''),
                button_link=request.POST.get('button_link', ''),
                is_active=request.POST.get('is_active') == 'on',
            )
            django_messages.success(request, 'Announcement created.')
        elif action == 'delete':
            Announcement.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Announcement deleted.')
        elif action == 'toggle':
            a = get_object_or_404(Announcement, pk=request.POST.get('id'))
            a.is_active = not a.is_active; a.save()
        return redirect('portfolio:dashboard_announcements')
    return render(request, 'dashboard/announcements.html', {'announcements': Announcement.objects.all()})


# ── STATS ──
@login_required(login_url='/dashboard/login/')
def dashboard_stats(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Statistic.objects.create(
                title=request.POST.get('title', ''),
                value=request.POST.get('value', ''),
                icon=request.POST.get('icon', ''),
                order=Statistic.objects.count(),
            )
            django_messages.success(request, 'Stat added.')
        elif action == 'edit':
            s = get_object_or_404(Statistic, pk=request.POST.get('id'))
            s.title = request.POST.get('title', s.title)
            s.value = request.POST.get('value', s.value)
            s.icon = request.POST.get('icon', s.icon)
            s.save()
            django_messages.success(request, 'Stat updated.')
        elif action == 'delete':
            Statistic.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Stat deleted.')
        return redirect('portfolio:dashboard_stats')
    return render(request, 'dashboard/stats.html', {'stats': Statistic.objects.all()})


# ── SERVICES ──
@login_required(login_url='/dashboard/login/')
def dashboard_services(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Service.objects.create(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                icon=request.POST.get('icon', ''),
                order=Service.objects.count(),
            )
            django_messages.success(request, 'Service added.')
        elif action == 'edit':
            s = get_object_or_404(Service, pk=request.POST.get('id'))
            s.title = request.POST.get('title', s.title)
            s.description = request.POST.get('description', s.description)
            s.icon = request.POST.get('icon', s.icon)
            s.save()
            django_messages.success(request, 'Service updated.')
        elif action == 'delete':
            Service.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Service deleted.')
        return redirect('portfolio:dashboard_services')
    return render(request, 'dashboard/services.html', {'services': Service.objects.all()})


# ── EXPERIENCE ──
@login_required(login_url='/dashboard/login/')
def dashboard_experience(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            from datetime import date
            end_date_str = request.POST.get('end_date', '')
            Experience.objects.create(
                title=request.POST.get('title', ''),
                company=request.POST.get('company', ''),
                start_date=request.POST.get('start_date'),
                end_date=end_date_str if end_date_str else None,
                is_current=request.POST.get('is_current') == 'on',
                description=request.POST.get('description', ''),
                order=Experience.objects.count(),
            )
            django_messages.success(request, 'Experience added.')
        elif action == 'delete':
            Experience.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Experience deleted.')
        return redirect('portfolio:dashboard_experience')
    return render(request, 'dashboard/experience.html', {'experiences': Experience.objects.all()})


# ── SOCIAL LINKS ──
@login_required(login_url='/dashboard/login/')
def dashboard_social(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            SocialLink.objects.create(
                platform=request.POST.get('platform', ''),
                url=request.POST.get('url', ''),
                order=SocialLink.objects.count(),
            )
            django_messages.success(request, 'Social link added.')
        elif action == 'edit':
            s = get_object_or_404(SocialLink, pk=request.POST.get('id'))
            s.url = request.POST.get('url', s.url)
            s.save()
            django_messages.success(request, 'Link updated.')
        elif action == 'delete':
            SocialLink.objects.filter(pk=request.POST.get('id')).delete()
            django_messages.success(request, 'Link deleted.')
        return redirect('portfolio:dashboard_social')
    return render(request, 'dashboard/social.html', {
        'social_links': SocialLink.objects.all(),
        'platforms': SocialLink.PLATFORM_CHOICES,
    })


# ── CONTACT INFO ──
@login_required(login_url='/dashboard/login/')
def dashboard_contact_info(request):
    if not request.user.is_staff: return redirect('portfolio:home')
    info = ContactInfo.objects.first()
    if request.method == 'POST':
        if not info:
            info = ContactInfo()
        info.email = request.POST.get('email', '')
        info.phone = request.POST.get('phone', '')
        info.address = request.POST.get('address', '')
        info.save()
        django_messages.success(request, 'Contact information updated. Email notifications will be sent to: ' + info.email)
        return redirect('portfolio:dashboard_contact_info')
    return render(request, 'dashboard/contact_info.html', {'info': info})
