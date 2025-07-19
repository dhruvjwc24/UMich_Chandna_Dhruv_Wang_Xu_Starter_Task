from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import User, Book

def index(request):
    users_all = User.objects.all()
    books_all = Book.objects.all()
    
    users_filtered = users_all
    books_filtered = books_all
    
    return render(request, "querydb/index.html", {
        "users_all": users_all,
        "books_all": books_all,
        "users_filtered": users_filtered,
        "books_filtered": books_filtered
    })

def filter_results(request):
    table = request.GET.get("table")
    users_all = User.objects.all()
    books_all = Book.objects.all()
    
    users_filtered = User.objects.none()
    books_filtered = Book.objects.none()

    if table == "User":
        users_filtered = users_all

        user_names = request.GET.getlist("user_names")
        age_op = request.GET.get("age_operator")  # single value
        age_val = request.GET.get("age_value")    # single value
        liked_books = request.GET.getlist("liked_books")

        if user_names:
            users_filtered = users_filtered.filter(name__in=user_names)

        if age_op and age_val:
            try:
                age_val = int(age_val)
                users_filtered = users_filtered.filter(**{f"age__{age_op}": age_val})
            except ValueError:
                pass  # silently skip invalid age input

        if liked_books:
            users_filtered = users_filtered.filter(liked_books__name__in=liked_books).distinct()

    elif table == "Book":
        books_filtered = books_all

        book_names = request.GET.getlist("book_names")
        price_op = request.GET.get("price_operator")
        price_val = request.GET.get("price_value")
        liked_by_users = request.GET.getlist("liked_by_users")

        if book_names:
            books_filtered = books_filtered.filter(name__in=book_names)

        if price_op and price_val:
            try:
                price_val = float(price_val)
                books_filtered = books_filtered.filter(**{f"price__{price_op}": price_val})
            except ValueError:
                pass

        if liked_by_users:
            books_filtered = books_filtered.filter(liked_by_users__name__in=liked_by_users).distinct()
        
    else:
        # If no valid table is selected, return all users and books
        users_filtered = users_all
        books_filtered = books_all

    return render(request, "querydb/index.html", {
        "users_all": users_all,
        "books_all": books_all,
        "users_filtered": users_filtered,
        "books_filtered": books_filtered
    })
        
def add_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        liked_books = request.POST.getlist("liked_books")
        
        if name and age:
            user = User.objects.create(name=name, age=int(age))
            if liked_books:
                user.liked_books.set(Book.objects.filter(name__in=liked_books))
    return redirect('filter_results')

def delete_user(request, user_id): 
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect('filter_results')

def add_book(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        liked_by_users = request.POST.getlist("liked_by_users")
        
        if name and price:
            book = Book.objects.create(name=name, price=float(price))
            if liked_by_users:
                book.liked_by_users.set(User.objects.filter(name__in=liked_by_users))
    return redirect('filter_results')

def delete_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        book.delete()
    return redirect('filter_results')

def save_edit_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        name = request.POST.get("name")
        age = request.POST.get("age")
        liked_books = request.POST.getlist("liked_books")

        if name:
            user.name = name
        if age:
            try:
                user.age = int(age)
            except ValueError:
                pass
        user.save()

        if liked_books:
            user.liked_books.set(Book.objects.filter(name__in=liked_books))
        else:
            user.liked_books.clear()

    return redirect("filter_results")

def save_edit_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        name = request.POST.get("name")
        price = request.POST.get("price")
        liked_by_users = request.POST.getlist("liked_by_users")

        if name:
            book.name = name
        if price:
            try:
                book.price = float(price)
            except ValueError:
                pass
        book.save()

        if liked_by_users:
            book.liked_by_users.set(User.objects.filter(name__in=liked_by_users))
        else:
            book.liked_by_users.clear()

    return redirect("filter_results")