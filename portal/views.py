from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document, Shipment
from .forms import DocumentForm, ShipmentForm
def home(request):
    return render(request,'portal/index.html')
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
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
@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request,'Portal/document_list.html', {'documents':documents})
@login_required
def document_upload(request):
    if request.method=='POST':
        form=DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document=form.save(commit=False)
            document.uploaded_by=request.user
            document.save()
            messages.success(request,'Document uploaded successfully')
            return redirect('document_list')
        else:
            form=DocumentForm()
        return render(request,'portal/document_upload.html',{'form':form})
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
