from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import random
import string

# Issue categories for Ward 11
ISSUE_TYPES = {
    'water': {'name': 'Water', 'emoji': '💧', 'color': '#3498db'},
    'electricity': {'name': 'Electricity', 'emoji': '⚡', 'color': '#f1c40f'},
    'roads': {'name': 'Roads/Potholes', 'emoji': '🛣️', 'color': '#95a5a6'},
}

# Status options for issue tracking
ISSUE_STATUSES = ['Received', 'In Progress', 'Fixed']

# Mock data for reported issues
REPORTED_ISSUES = []


def generate_reference_number(issue_type=''):
    """Generate unique reference number like W11-WATER-089"""
    prefix = 'W11'
    type_abbrev = issue_type[:1].upper() if issue_type else 'R'
    random_digits = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}-{type_abbrev}-{random_digits}"


def home_view(request):
    """Home/Dashboard with issue category icons - VILLAGE FILTERED"""
    # Check if user is logged in
    user_email = request.session.get('user_email', None)
    user_village = request.session.get('user_village', None)
    
    if not user_email or not user_village:
        # Redirect to login if no session data
        return redirect('/login/')
    
    # ALGORITHM: Filter reports by user's village ONLY
    village_reports = [r for r in REPORTED_ISSUES 
                      if r.get('village') == user_village]
    recent_reports = village_reports[-5:]  # Show last 5 reports from this village
    
    context = {
        'issue_types': ISSUE_TYPES,
        'recent_reports': recent_reports,
        'user_email': user_email,
        'user_village': user_village,
        'total_reports': len(village_reports),  # Show count of user's village reports
    }
    return render(request, 'services/home.html', context)


def report_issue_view(request):
    """Quick issue reporting page with form validation"""
    issue_type = request.GET.get('type', 'water')
    user_village = request.session.get('user_village', None)
    user_email = request.session.get('user_email', None)
    
    # Redirect to login if no session
    if not user_email or not user_village:
        return redirect('/login/')
    
    context = {
        'issue_types': ISSUE_TYPES,
        'selected_type': issue_type,
        'reference_number': None,
        'user_village': user_village,
    }
    
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        issue_type = request.POST.get('issue_type', 'water')
        
        # VALIDATION: Description field required
        if not description:
            context['error'] = 'Please describe the issue'
            return render(request, 'services/report_issue.html', context)
        
        # Generate reference number with type prefix
        reference = generate_reference_number(issue_type)
        
        # STORE REPORT with enhanced data
        new_report = {
            'reference': reference,
            'type': issue_type,
            'status': 'Received',
            'description': description,
            'village': user_village,  # ENFORCE: Store user's village
            'email': user_email,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'status_history': ['Received'],  # Track status changes
        }
        
        REPORTED_ISSUES.append(new_report)
        
        context['reference_number'] = reference
        context['submitted'] = True
        context['success_message'] = f'Report {reference} submitted successfully'
    
    return render(request, 'services/report_issue.html', context)


def track_status_view(request):
    """Enhanced status tracking with timeline and feedback - VILLAGE FILTERED"""
    reference = request.GET.get('ref', '').strip()
    user_village = request.session.get('user_village', None)
    issue = None
    error = None
    
    # VALIDATION: User must be logged in
    if not user_village:
        return redirect('/login/')
    
    if reference:
        # Search for matching reference
        for rep in REPORTED_ISSUES:
            if rep['reference'].upper() == reference.upper():
                # SECURITY: Only show reports from user's village
                if rep['village'] == user_village:
                    issue = rep
                else:
                    error = 'Report not found or access denied'
                break
        
        if not issue and not error:
            error = f'No report found with reference: {reference}'
    
    # Format timestamps for display
    if issue and issue.get('created_at'):
        issue['created_time'] = issue['created_at'].strftime('%B %d, %Y at %I:%M %p')
        issue['updated_time'] = issue['updated_at'].strftime('%I:%M %p')
    
    # Determine status timeline progress (0-100%)
    status_index = ISSUE_STATUSES.index(issue['status']) if issue else 0
    progress = int((status_index + 1) / len(ISSUE_STATUSES) * 100)
    
    # Status-specific next steps
    status_messages = {
        'Received': '✓ We received your report. A service team will contact you within 24 hours.',
        'In Progress': '⚙️ Our team is working on this. Estimated completion: 5 days.',
        'Fixed': '✅ Issue resolved! Thank you for reporting to Ward 11.',
    }
    
    context = {
        'issue': issue,
        'reference': reference,
        'error': error,
        'user_village': user_village,
        'progress': progress,
        'status_message': status_messages.get(issue['status'], '') if issue else '',
        'all_statuses': ISSUE_STATUSES,
    }
    return render(request, 'services/track_status.html', context)
