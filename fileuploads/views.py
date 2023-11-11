from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .forms import UploadFileForm

from django.core.paginator import Paginator

from .models import UploadedFile

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UploadedFile

def homepage(request):
    versions = UploadedFile.objects.order_by('-uploaded_at')
    paginator = Paginator(versions, 7)  # Show 7 versions per page
    page = request.GET.get('page')
    try:
        versions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        versions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        versions = paginator.page(paginator.num_pages)
    return render(request, 'homepage.html', {'versions': versions})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.all().order_by('-uploaded_at')

    paginator = Paginator(files, 7)  # Show 7 versions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'upload_file.html', {'form': form, 'page_obj': page_obj})


def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    return FileResponse(file.file, as_attachment=True, filename=file.file.name)
