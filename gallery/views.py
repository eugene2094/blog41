from django.shortcuts import render, redirect

# Create your views here.
# from blog.views import get_categories
from .forms import PhotoForm
from .models import Photo


def gallery(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    # context.update(get_categories())
    return render(request, "gallery/index.html", context)


def uploads(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    form = PhotoForm()
    return render(request, 'gallery/upload.html', {'form': form})
