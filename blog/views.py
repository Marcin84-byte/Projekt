from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogPostModelForm
from .models import BlogPost


def blog_post_detail_view(request, slug):
    post_view = get_object_or_404(BlogPost, slug=slug)
    context = {"object": post_view}

    return render(request, 'detail.html', context)


@login_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect("list_blog")

    context = {'form': form}
    return render(request, 'create.html', context)


@login_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect("post_detail", slug=slug)

    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, 'form.html', context)


@login_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        obj.delete()
        return redirect("home")

    context = {"object": obj}
    return render(request, 'delete.html', context)
