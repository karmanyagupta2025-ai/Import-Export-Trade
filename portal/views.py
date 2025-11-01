from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document
from .forms import DocumentForm
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


# Create your views here.
