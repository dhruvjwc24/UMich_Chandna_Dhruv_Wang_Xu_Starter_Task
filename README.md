# AI Annotation Assistant and Database Query Manager
_This is a repository containing my work for building an AI Annotation Assistant and a Database Query Manager. Please keep reading for initializing this repository into your local machine, along with further steps on running and interacting with the projects!_

## Git Initialization
1. Open your device terminal and navigate to a directory of your choosing. 
2. In the terminal, execute `mkdir UMich_Chandna_Dhruv_Wang_Xu_Starter_Task_Fork`

```
# Run this in Django shell: python manage.py shell

from querydb.models import User, Book

# Clear existing data
User.objects.all().delete()
Book.objects.all().delete()

# Fixed names and titles
first_names = [
    "Aiden", "Maya", "Leo", "Zoe", "Noah", "Ava", "Eli", "Isla",
    "Omar", "Ruby", "Luca", "Nia", "Theo", "Mira", "Kian"
]

book_titles = [
    "The Silent Patient", "Where the Crawdads Sing", "Little Fires Everywhere",
    "The Midnight Library", "A Man Called Ove", "The Book Thief", "Circe",
    "Verity", "The Night Circus", "Educated", "Before We Were Strangers",
    "The Paper Palace", "Ugly Love", "The Four Winds", "Reminders of Him"
]

# Fixed prices and ages
book_prices = [
    19.99, 15.50, 12.25, 21.75, 9.99, 17.40, 22.30, 14.95,
    18.60, 13.20, 8.80, 20.10, 10.50, 16.75, 11.95
]

user_ages = [
    25, 34, 19, 42, 30, 23, 27, 35,
    21, 28, 40, 22, 31, 26, 29
]

# Create books with fixed prices
books = []
for title, price in zip(book_titles, book_prices):
    book = Book.objects.create(name=title, price=price)
    books.append(book)

# Create users with fixed ages and assign liked books deterministically
for idx, (name, age) in enumerate(zip(first_names, user_ages)):
    user = User.objects.create(name=name, age=age)
    liked = books[idx % 15: (idx % 15) + (idx % 10) + 1]
    user.liked_books.set(liked)

print("Database successfully populated with reproducible users and books.")
```
