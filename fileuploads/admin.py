from django.contrib import admin

# Register your models here.
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.contrib import admin
from .models import UploadedFile

admin.site.register(UploadedFile)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.all()
    return render(request, 'upload_file.html', {'form': form, 'files': files})
