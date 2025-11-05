from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, login as auth_login, logout
from .forms import DocumentForm, ShipmentForm
from .models import Document, Shipment


# ==================== HOME & AUTH VIEWS ====================

@login_required
def home(request):
    """Dynamic homepage with shipment statistics"""
    # Get recent shipments
    recent_shipments = Shipment.objects.all().order_by('-created_at')[:5]
    
    # Get statistics
    total_shipments = Shipment.objects.count()
    in_transit = Shipment.objects.filter(status='in_transit').count()
    delivered = Shipment.objects.filter(status='delivered').count()
    pending = Shipment.objects.filter(status='pending').count()
    customs = Shipment.objects.filter(status='customs').count()
    
    # Get total documents
    total_documents = Document.objects.count()
    
    context = {
        'recent_shipments': recent_shipments,
        'total_shipments': total_shipments,
        'in_transit': in_transit,
        'delivered': delivered,
        'pending': pending,
        'customs': customs,
        'total_documents': total_documents,
    }
    
    return render(request, 'portal/index.html', context)


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Redirect based on user role
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    
    return render(request, 'portal/login.html')


def signup(request):
    """User signup view"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'portal/signup.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# ==================== DASHBOARD VIEWS ====================

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with system overview"""
    # Get statistics
    total_shipments = Shipment.objects.count()
    total_documents = Document.objects.count()
    total_clients = User.objects.count()
    # Shipment status counts
    pending = Shipment.objects.filter(status='pending').count()
    in_transit = Shipment.objects.filter(status='in_transit').count()
    delivered = Shipment.objects.filter(status='delivered').count()
    customs = Shipment.objects.filter(status='customs').count()
    
    # Recent activity
    recent_shipments = Shipment.objects.all().order_by('-created_at')[:5]
    recent_documents = Document.objects.all().order_by('-uploaded_at')[:5]
    
    context = {
        'total_shipments': total_shipments,
        'total_documents': total_documents,
        'pending': pending,
        'in_transit': in_transit,
        'delivered': delivered,
        'customs': customs,
        'recent_shipments': recent_shipments,
        'recent_documents': recent_documents,
    }
    
    return render(request, 'portal/admin_dashboard.html', context)
@login_required
def client_dashboard(request):
    """Client dashboard - view their own shipments and documents"""
    # Get user's shipments (if you want to filter by user)
    # For now, showing all shipments
    recent_shipments = Shipment.objects.all().order_by('-created_at')[:5]
    
    # Get user's documents
    user_documents = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')[:5]
    
    # Statistics
    total_shipments = Shipment.objects.count()
    in_transit = Shipment.objects.filter(status='in_transit').count()
    delivered = Shipment.objects.filter(status='delivered').count()
    
    # ADD THIS LINE:
    total_clients = User.objects.count()
    
    context = {
        'recent_shipments': recent_shipments,
        'user_documents': user_documents,
        'total_shipments': total_shipments,
        'in_transit': in_transit,
        'delivered': delivered,
        'total_clients': total_clients,  # ADD THIS LINE
    }
    
    return render(request, 'portal/client_dashboard.html', context)




# ==================== DOCUMENT VIEWS ====================

@login_required
def document_list(request):
    """List all documents"""
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'portal/document_list.html', {'documents': documents})


@login_required
def document_upload(request):
    """Upload new document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('document_list')
    else:
        form = DocumentForm()
    
    return render(request, 'portal/document_upload.html', {'form': form})


@login_required
def document_delete(request, pk):
    """Delete document"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('document_list')
    
    return render(request, 'portal/document_confirm_delete.html', {'document': document})


# ==================== SHIPMENT VIEWS ====================

@login_required
def shipment_list(request):
    """List all shipments"""
    shipments = Shipment.objects.all().order_by('-created_at')
    return render(request, 'portal/shipment_list.html', {'shipments': shipments})


@login_required
def shipment_create(request):
    """Create new shipment"""
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, f'Shipment {shipment.tracking_number} created successfully!')
            return redirect('shipment_list')
    else:
        form = ShipmentForm()
    
    return render(request, 'portal/shipment_form.html', {'form': form, 'action': 'Create'})


@login_required
def shipment_detail(request, pk):
    """View shipment details"""
    shipment = get_object_or_404(Shipment, pk=pk)
    return render(request, 'portal/shipment_detail.html', {'shipment': shipment})


@login_required
def shipment_update(request, pk):
    """Update existing shipment"""
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Shipment {shipment.tracking_number} updated successfully!')
            return redirect('shipment_detail', pk=shipment.pk)
    else:
        form = ShipmentForm(instance=shipment)
    
    return render(request, 'portal/shipment_form.html', {
        'form': form, 
        'action': 'Update', 
        'shipment': shipment
    })


@login_required
def shipment_delete(request, pk):
    """Delete shipment"""
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        tracking_number = shipment.tracking_number
        shipment.delete()
        messages.success(request, f'Shipment {tracking_number} deleted successfully!')
        return redirect('shipment_list')
    
    return render(request, 'portal/shipment_confirm_delete.html', {'shipment': shipment})
