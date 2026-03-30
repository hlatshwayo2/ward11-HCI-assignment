from django.shortcuts import render
from django.http import HttpResponse
import random
import string

# Issue categories for Ward 11
ISSUE_TYPES = {
    'water': {'name': 'Water', 'emoji': '💧', 'color': '#3498db'},
    'electricity': {'name': 'Electricity', 'emoji': '⚡', 'color': '#f1c40f'},
    'roads': {'name': 'Roads/Potholes', 'emoji': '🛣️', 'color': '#95a5a6'},
}

# Mock data for reported issues
REPORTED_ISSUES = []


def generate_reference_number():
    """Generate unique reference number like W11-WATER-089"""
    prefix = 'W11'
    random_digits = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}-{random_digits}"


def home_view(request):
    """Home/Dashboard with issue category icons"""
    # Get user info from session
    user_email = request.session.get('user_email', 'Guest')
    user_village = request.session.get('user_village', 'Select Village')
    
    context = {
        'issue_types': ISSUE_TYPES,
        'recent_reports': REPORTED_ISSUES[-5:],  # Show last 5 reports
        'user_email': user_email,
        'user_village': user_village,
    }
    return render(request, 'services/home.html', context)


def report_issue_view(request):
    """Quick issue reporting page"""
    issue_type = request.GET.get('type', 'water')
    context = {
        'issue_types': ISSUE_TYPES,
        'selected_type': issue_type,
        'reference_number': None
    }
    
    if request.method == 'POST':
        # Mock submission
        reference = generate_reference_number()
        context['reference_number'] = reference
        context['submitted'] = True
        
        # Store in mock data
        REPORTED_ISSUES.append({
            'reference': reference,
            'type': issue_type,
            'status': 'Received',
            'description': request.POST.get('description', '')
        })
    
    return render(request, 'services/report_issue.html', context)


def track_status_view(request):
    """Track report status by reference number"""
    reference = request.GET.get('ref', '')
    issue = None
    
    for rep in REPORTED_ISSUES:
        if rep['reference'] == reference:
            issue = rep
            break
    
    context = {'issue': issue, 'reference': reference}
    return render(request, 'services/track_status.html', context)
