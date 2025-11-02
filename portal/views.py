from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DocumentForm, ShipmentForm, TradeForm
from .models import Document, Shipment, Trade



def home(request):
    return render(request,'portal/index.html')
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request,'portal/login.html')
def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request,'portal/signup.html',{'form': form})
def client_dashboard(request):
    trades=Trade.objects.filter(user=request.user).order_by('-date')
    return render(request,'portal/client_dashboard.html',{'trades':trades})
@staff_member_required
def admin_dashboard(request):
    return render(request,'portal/admin_dashboard.html')
@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request,'portal/document_list.html', {'documents':documents})
@login_required
def document_upload(request):
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
def document_delete(request,pk):
    document=get_object_or_404(Document, pk=pk)
    if request.method=='POST':
        document.delete()
        messages.success(request,'Document deleted successfully!')
        return redirect ('document_list')
    return render(request, 'portal/document_confirm_delete.html',{'document': document})
# Shipment tracking views
@login_required
def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, 'portal/shipment_list.html', {'shipments': shipments})

@login_required
def shipment_create(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, 'Shipment created successfully!')
            return redirect('shipment_list')
    else:
        form = ShipmentForm()
    return render(request, 'portal/shipment_form.html', {'form': form, 'action': 'Create'})

@login_required
def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    return render(request, 'portal/shipment_detail.html', {'shipment': shipment})

@login_required
def shipment_update(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipment updated successfully!')
            return redirect('shipment_detail', pk=shipment.pk)
    else:
        form = ShipmentForm(instance=shipment)
    return render(request, 'portal/shipment_form.html', {'form': form, 'action': 'Update', 'shipment': shipment})

@login_required
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        shipment.delete()
        messages.success(request, 'Shipment deleted successfully!')
        return redirect('shipment_list')
    return render(request, 'portal/shipment_confirm_delete.html', {'shipment': shipment})


# Create your views here.
@login_required
def trade_entry(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade= form.save(commit=False)
            trade.user=request.user
            trade.save()
            messages.success(request,'Trade entry created successfully!')
            return redirect('client_dashboard')
    else:
        form=TradeForm()
    return render(request,'portal/trade_entry.html', {'form': form})
