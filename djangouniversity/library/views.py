from typing import Dict

from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from .models import Book, Author, Category, Place, Language
from .forms import BookForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q, QuerySet


class MainView(View):
    template_name = 'library/book_list.html'

    def get(self, request):

        strval = request.GET.get("search", False)
        if strval:
            query = Q(name__icontains=strval)
            query.add(Q(description__icontains=strval), Q.OR)
            book_list = Book.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            book_list = Book.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in book_list:
            obj.natural_updated = naturaltime(obj.updated_at)
        # print(connection.queries)
        lb = Book.objects.all()
        la = Author.objects.count()
        ctx = {'book_list': book_list, 'search': strval, 'author_count': la}
        return render(request, self.template_name, ctx)
        # print(connection.queries)


class BookListView(ListView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class BookCreateView(OwnerCreateView):
    model = Book

    fields = ['name', 'category', 'description']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:all')

    def get(self, request, pk=None):
        form = BookForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = BookForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

            # Add owner to the model before saving
        book = form.save(commit=False)
        book.owner = self.request.user
        book.save()
        # form.save_m2m()    # Add this
        return redirect(self.success_url)


class BookUpdateView(OwnerUpdateView):
    template_name = 'library/book_form.html'
    model = Book
    # fields = '__all__'
    success_url = reverse_lazy('library:all')

    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        form = BookForm(instance=book)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        book = get_object_or_404(Book, id=pk)
        # , owner=self.request.user)
        form = BookForm(request.POST, request.FILES or None, instance=book)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        book = form.save(commit=False)
        book.save()
        # form.save_m2m()    # Add this

        return redirect(self.success_url)


class BookDeleteView(DeleteView):
    model = Book
    fields = fields = '__all__'
    success_url = reverse_lazy('library:all')


class BookDetailView(OwnerDetailView):
    model = Book
    template_name = "library/book_detail.html"

    def get(self, request, pk):
        x = Book.objects.get(id=pk)
        # comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        # comment_form = CommentForm()
        context = {'book': x}
        return render(request, self.template_name, context)


class LanguageView(View):
    def get(self, request):
        ml = Language.objects.all()
        ctx = {'language_list': ml}
        return render(request, 'library/language_list.html', ctx)


class LanguageCreateView(CreateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class LanguageUpdateView(UpdateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class LanguageDeleteView(DeleteView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceView(View):
    def get(self, request):
        pl = Place.objects.all()
        ctx = {'place_list': pl}
        return render(request, 'library/place_list.html', ctx)


class PlaceCreateView(CreateView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceUpdateView(UpdateView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceDeleteView(DeleteView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryView(View):
    def get(self, request):
        cl = Category.objects.all()
        ctx = {'category_list': cl}
        return render(request, 'library/category_list.html', ctx)


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryDeleteView(DeleteView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class AuthorView(View):
    def get(self, request):
        al = Author.objects.all()
        ctx = {'author_list': al}
        return render(request, 'library/author_list.html', ctx)


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class AuthorDeleteView(DeleteView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"


def stream_file(request, pk):
    book = get_object_or_404(Book, id=pk)
    response = HttpResponse()
    response['Content-Type'] = book.content_type
    response['Content-Length'] = len(book.picture)
    response.write(book.picture)
    return response