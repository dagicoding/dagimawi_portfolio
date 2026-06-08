#!/bin/bash
# ============================================
# Dagimawi Tarekegne Portfolio - Setup Script
# ============================================
set -e

echo ""
echo "============================================"
echo "  Dagimawi Tarekegne Portfolio Setup"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON=$(command -v python3)
echo "[OK] Python: $($PYTHON --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[...] Creating virtual environment..."
    $PYTHON -m venv venv
fi
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || true
echo "[OK] Virtual environment ready"

# Install dependencies
echo "[...] Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "[OK] Dependencies installed"

# Migrations
echo "[...] Running migrations..."
python manage.py makemigrations portfolio --noinput 2>/dev/null || true
python manage.py migrate
echo "[OK] Database ready"

# Seed default data
echo "[...] Seeding default data..."
python manage.py shell << 'PYEOF'
from portfolio.models import (
    HomeProfile, Role, Skill, Statistic, SocialLink,
    PortfolioCategory, ContactInfo, Service
)

if not HomeProfile.objects.exists():
    HomeProfile.objects.create(
        name="Dagimawi Tarekegne",
        description="Passionate about creating stunning visual experiences through innovative design, compelling video editing, and engaging content creation."
    )
    print("  -> Home profile created")

roles = ["Graphic Designer", "Video Editor", "Content Creator", "Brand Designer"]
for i, r in enumerate(roles):
    Role.objects.get_or_create(title=r, defaults={'order': i})
print("  -> Roles seeded")

skills_data = [
    ("Adobe Photoshop", 95, "bi bi-brush"),
    ("Adobe Illustrator", 90, "bi bi-vector-pen"),
    ("Adobe Premiere Pro", 88, "bi bi-film"),
    ("After Effects", 82, "bi bi-stars"),
    ("Canva", 92, "bi bi-grid"),
    ("Content Creation", 90, "bi bi-camera"),
]
for i, (name, pct, icon) in enumerate(skills_data):
    Skill.objects.get_or_create(name=name, defaults={'percentage': pct, 'icon': icon, 'order': i})
print("  -> Skills seeded")

stats = [("Projects Completed","50+"),("Happy Clients","20+"),("Years Experience","3+"),("Designs Created","100+")]
for i, (t, v) in enumerate(stats):
    Statistic.objects.get_or_create(title=t, defaults={'value': v, 'order': i})
print("  -> Stats seeded")

cats = [("Poster Design","poster-design"),("Thumbnail Design","thumbnail-design"),("Logo Design","logo-design"),("Video Editing","video-editing")]
for i, (name, slug) in enumerate(cats):
    PortfolioCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'order': i})
print("  -> Categories seeded")

if not ContactInfo.objects.exists():
    ContactInfo.objects.create(email="dagimawi@example.com", phone="+251 900 000 000", address="Addis Ababa, Ethiopia")
    print("  -> Contact info created")

services_data = [
    ("Graphic Design","Professional graphic design services including posters, flyers, and social media graphics.","bi bi-brush"),
    ("Logo Design","Unique and memorable logo designs that represent your brand identity.","bi bi-vector-pen"),
    ("Video Editing","Professional video editing with cinematic effects and color grading.","bi bi-film"),
    ("Content Creation","Engaging content for YouTube, TikTok, Instagram, and other platforms.","bi bi-camera"),
    ("Thumbnail Design","Click-worthy thumbnails designed to maximize engagement.","bi bi-grid"),
    ("Brand Identity","Complete brand packages including logos, color palettes, and guidelines.","bi bi-star"),
]
for i, (title, desc, icon) in enumerate(services_data):
    Service.objects.get_or_create(title=title, defaults={'description': desc, 'icon': icon, 'order': i})
print("  -> Services seeded")
PYEOF

# Collect static
echo "[...] Collecting static files..."
python manage.py collectstatic --noinput -v 0
echo "[OK] Static files collected"

# Superuser
echo ""
echo "============================================"
echo "  Create Admin User"
echo "============================================"
read -p "Create a superuser now? (y/n): " CREATE_SUPER
if [[ "$CREATE_SUPER" == "y" || "$CREATE_SUPER" == "Y" ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "  Run the server:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Then open:"
echo "    Website:          http://127.0.0.1:8000/"
echo "    Custom Dashboard: http://127.0.0.1:8000/dashboard/"
echo "    Django Admin:     http://127.0.0.1:8000/admin/"
echo ""
echo "  Email notifications:"
echo "    1. Open dagimawi_portfolio/settings.py"
echo "    2. Uncomment the Gmail SMTP block"
echo "    3. Add your Gmail address + App Password"
echo "    4. Set your recipient email in Dashboard > Contact Info"
echo ""
