from django.shortcuts import render, redirect
from django.http import HttpResponse

# Ward 11 sub-communities
VILLAGES = [
    'Hambrook Village',
    'Acton Homes Village',
    'Greenpoint Village',
    'Malotha Village',
    'KwaPikinini Village',
]

# Mock user database
REGISTERED_USERS = {}


def login_view(request):
    """User login page with village selection"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        village = request.POST.get('village')
        
        # Simple validation (mock authentication)
        if email and password and village:
            # Store in session (for demo purposes)
            request.session['user_email'] = email
            request.session['user_village'] = village
            # Redirect to home page after successful login
            return redirect('/')
        else:
            context = {'villages': VILLAGES, 'error': 'Please fill all fields'}
            return render(request, 'accounts/login.html', context)
    
    context = {'villages': VILLAGES}
    return render(request, 'accounts/login.html', context)


def register_view(request):
    """User registration page with village selection"""
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        village = request.POST.get('village')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if not all([fullname, email, village, password, confirm_password]):
            context = {'villages': VILLAGES, 'error': 'Please fill all required fields'}
            return render(request, 'accounts/register.html', context)
        
        if password != confirm_password:
            context = {'villages': VILLAGES, 'error': 'Passwords do not match'}
            return render(request, 'accounts/register.html', context)
        
        # Store user (mock registration)
        REGISTERED_USERS[email] = {
            'fullname': fullname,
            'village': village,
            'password': password
        }
        
        # Redirect to login after successful registration
        return redirect('/login/')
    
    context = {'villages': VILLAGES}
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    """Logout user and clear session"""
    # Clear session data
    request.session.flush()
    # Redirect to login page
    return redirect('/login/')
