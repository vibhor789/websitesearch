#!/usr/bin/env python3
"""
Website Search & Chatbox Finder - Web Dashboard
A SaaS-ready web application for lead generation
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import json
import csv
from io import StringIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///websearch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ========== DATABASE MODELS ==========

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    searches = db.relationship('Search', backref='user', lazy=True)

    # User settings
    openai_api_key = db.Column(db.String(200))
    anthropic_api_key = db.Column(db.String(200))
    scraper_api_key = db.Column(db.String(200))
    default_ai_provider = db.Column(db.String(20), default='openai')
    default_screenshots = db.Column(db.Boolean, default=False)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    max_results = db.Column(db.Integer, default=10)
    screenshots_enabled = db.Column(db.Boolean, default=False)
    ai_provider = db.Column(db.String(20), default='openai')
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    total_sites = db.Column(db.Integer, default=0)
    leads_found = db.Column(db.Integer, default=0)
    estimated_cost = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float, default=0.0)
    results = db.relationship('Lead', backref='search', lazy=True)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'), nullable=False)
    domain = db.Column(db.String(200))
    url = db.Column(db.String(500))
    business_type = db.Column(db.String(100))
    business_description = db.Column(db.Text)
    has_chatbox = db.Column(db.Boolean, default=False)
    has_whatsapp = db.Column(db.Boolean, default=False)
    has_call_button = db.Column(db.Boolean, default=False)
    detected_widgets = db.Column(db.Text)
    missing_features = db.Column(db.Text)
    recommended_features = db.Column(db.Text)
    priority = db.Column(db.String(20))
    recommendations = db.Column(db.Text)
    potential_impact = db.Column(db.Text)
    screenshot_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== ROUTES ==========

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent searches
    searches = Search.query.filter_by(user_id=current_user.id).order_by(Search.created_at.desc()).limit(10).all()

    # Stats
    total_searches = Search.query.filter_by(user_id=current_user.id).count()
    total_leads = db.session.query(db.func.sum(Search.leads_found)).filter_by(user_id=current_user.id).scalar() or 0
    total_cost = db.session.query(db.func.sum(Search.actual_cost)).filter_by(user_id=current_user.id).scalar() or 0

    return render_template('dashboard.html',
                          searches=searches,
                          total_searches=total_searches,
                          total_leads=total_leads,
                          total_cost=total_cost)

@app.route('/new-search', methods=['GET', 'POST'])
@login_required
def new_search():
    if request.method == 'POST':
        query = request.form.get('query')
        max_results = int(request.form.get('max_results', 10))
        screenshots_enabled = request.form.get('screenshots_enabled') == 'on'
        ai_provider = request.form.get('ai_provider', 'openai')

        # Check if user has API keys configured
        if ai_provider == 'openai' and not current_user.openai_api_key:
            flash('Please configure your OpenAI API key in Settings first', 'error')
            return redirect(url_for('settings'))

        if ai_provider == 'anthropic' and not current_user.anthropic_api_key:
            flash('Please configure your Anthropic API key in Settings first', 'error')
            return redirect(url_for('settings'))

        # Estimate cost
        cost_per_site = 0.012 if screenshots_enabled else 0.003
        estimated_cost = max_results * cost_per_site * 0.7  # Assume 70% need analysis

        # Create search record
        new_search = Search(
            user_id=current_user.id,
            query=query,
            max_results=max_results,
            screenshots_enabled=screenshots_enabled,
            ai_provider=ai_provider,
            status='pending',
            estimated_cost=estimated_cost
        )
        db.session.add(new_search)
        db.session.commit()

        flash(f'Search queued! Estimated cost: ${estimated_cost:.2f}', 'success')

        # In production, this would trigger a background task
        # For now, redirect to search detail page
        return redirect(url_for('search_detail', search_id=new_search.id))

    return render_template('new_search.html',
                          default_ai=current_user.default_ai_provider,
                          default_screenshots=current_user.default_screenshots)

@app.route('/search/<int:search_id>')
@login_required
def search_detail(search_id):
    search = Search.query.get_or_404(search_id)

    # Security check
    if search.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    leads = Lead.query.filter_by(search_id=search_id).all()

    return render_template('search_detail.html', search=search, leads=leads)

@app.route('/search/<int:search_id>/export')
@login_required
def export_search(search_id):
    search = Search.query.get_or_404(search_id)

    if search.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    leads = Lead.query.filter_by(search_id=search_id).all()

    # Create CSV
    output = StringIO()
    writer = csv.writer(output)

    # Headers
    writer.writerow([
        'Domain', 'URL', 'Business Type', 'Description',
        'Has Chatbox', 'Has WhatsApp', 'Has Call Button',
        'Missing Features', 'Recommended Features', 'Priority',
        'Recommendations', 'Potential Impact'
    ])

    # Data
    for lead in leads:
        writer.writerow([
            lead.domain, lead.url, lead.business_type, lead.business_description,
            'Yes' if lead.has_chatbox else 'No',
            'Yes' if lead.has_whatsapp else 'No',
            'Yes' if lead.has_call_button else 'No',
            lead.missing_features, lead.recommended_features, lead.priority,
            lead.recommendations, lead.potential_impact
        ])

    output.seek(0)

    return send_file(
        StringIO(output.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'leads_{search.query}_{search.id}.csv'
    )

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.openai_api_key = request.form.get('openai_api_key') or current_user.openai_api_key
        current_user.anthropic_api_key = request.form.get('anthropic_api_key') or current_user.anthropic_api_key
        current_user.scraper_api_key = request.form.get('scraper_api_key') or current_user.scraper_api_key
        current_user.default_ai_provider = request.form.get('default_ai_provider', 'openai')
        current_user.default_screenshots = request.form.get('default_screenshots') == 'on'

        db.session.commit()
        flash('Settings saved!', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html')

@app.route('/api/calculate-cost', methods=['POST'])
@login_required
def calculate_cost():
    data = request.get_json()
    max_results = data.get('max_results', 10)
    screenshots = data.get('screenshots', False)
    ai_provider = data.get('ai_provider', 'openai')

    # Cost calculation
    if ai_provider == 'openai':
        vision_cost = 0.01 if screenshots else 0
        text_cost = 0.002
    else:  # anthropic
        vision_cost = 0.008 if screenshots else 0
        text_cost = 0.0015

    cost_per_site = vision_cost + text_cost
    # Assume 70% of sites need analysis (30% already have chatboxes)
    estimated_cost = max_results * cost_per_site * 0.7

    return jsonify({
        'cost_per_site': cost_per_site,
        'estimated_cost': round(estimated_cost, 4),
        'max_results': max_results
    })

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# ========== API ENDPOINTS FOR BACKGROUND TASKS ==========

@app.route('/api/run-search/<int:search_id>', methods=['POST'])
@login_required
def run_search_api(search_id):
    """API endpoint to start a search (called by background worker)"""
    search = Search.query.get_or_404(search_id)

    if search.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403

    # Mark as running
    search.status = 'running'
    db.session.commit()

    # In production, this would trigger the actual search
    # For now, return success
    return jsonify({'status': 'started', 'search_id': search_id})

# ========== MAIN ==========

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
