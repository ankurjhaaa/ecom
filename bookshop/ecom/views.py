from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import *
from django.utils.text import slugify
from .forms import AuthorInsertForm, GenereInsertForm, BookInsertForm

# Create your views here.

def home(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    if search:
        isbn_books = Book.objects.filter(isbn=search)
        if isbn_books.exists():
            return render(request, 'book_view.html', {
                "title": isbn_books.first().title,
                "book": isbn_books.first(),
                "related_books": Book.objects.filter(genere=isbn_books.first().genere).exclude(id=isbn_books.first().id)[:4],
                "generes" : Genere.objects.all(),
            })
        else:
            books = Book.objects.filter(title__icontains=search)

    elif category:
        books = Book.objects.filter(genere__slug=category)
    elif search:
        books = Book.objects.filter(title__icontains=search)
    else:
        books = Book.objects.all()
    data = {
        "title": "Home",
        "generes" : Genere.objects.all(),
        "books" : books,
    }
    return render(request, 'home.html', data)

def filter(request):
    return render(request, 'filter.html')

def book_view(request, slug):
    book = Book.objects.get(slug=slug)
    related_books = Book.objects.filter(genere=book.genere).exclude(id=book.id)[:4]
    data = {
        "title": book.title,
        "book": book,
        "related_books": related_books,
        "generes" : Genere.objects.all(),
    }
    return render(request, 'book_view.html', data)


def admin_dashboard(request):
    data = {
        "title": "Admin Dashboard",
        "total_books": Book.objects.count(),
        "total_authors": Author.objects.count(),
        "total_genres": Genere.objects.count(),
    }
    return render(request, 'admin/dashboard.html', data)


def admin_books(request): 
    if request.method == "POST":
        book_form = BookInsertForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            base_slug = slugify(book.title)
            slug = base_slug

            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            book.slug = slug
            book.save()
            return redirect("admin_books")
    else:
        book_form = BookInsertForm()

    books_list = Book.objects.select_related("author", "genere").all().order_by("-id")
    paginator = Paginator(books_list, 10)
    page_number = request.GET.get('page', 1)
    books = paginator.get_page(page_number)

    data = {
        "title": "Admin Books",
        "books": books,
        "book_form": book_form,
        "paginator": paginator,
        "page_obj": books,
    }
    return render(request, 'admin/products.html', data)


def admin_authors(request):
    if request.method == "POST":
        author_form = AuthorInsertForm(request.POST or None)
        if author_form.is_valid():
            author = author_form.save(commit=False)
            base_slug = slugify(author.name)
            slug = base_slug

            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            author.slug = slug
            author.save()
            return redirect("admin_authors")
    else:
        author_form = AuthorInsertForm()

    authors_list = Author.objects.all().order_by('-id')
    paginator = Paginator(authors_list, 10)
    page_number = request.GET.get('page', 1)
    authors = paginator.get_page(page_number)

    data = {
        "title": "Admin Authors",
        "authors": authors,
        "author_form": author_form,
        "paginator": paginator,
        "page_obj": authors,
    }

    return render(request, 'admin/authors.html', data)


def admin_generes(request):
    if request.method == "POST":
        genere_form = GenereInsertForm(request.POST)
        if genere_form.is_valid():
            genere = genere_form.save(commit=False)
            base_slug = slugify(genere.title)
            slug = base_slug

            counter = 1
            while Genere.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            genere.slug = slug
            genere.save()
            return redirect("admin_generes")
    else:
        genere_form = GenereInsertForm()

    genres_list = Genere.objects.all().order_by("-id")
    paginator = Paginator(genres_list, 10)
    page_number = request.GET.get('page', 1)
    genres = paginator.get_page(page_number)

    data = {
        "title": "Admin Generes",
        "genres": genres,
        "genere_form": genere_form,
        "paginator": paginator,
        "page_obj": genres,
    }
    return render(request, 'admin/generes.html', data)