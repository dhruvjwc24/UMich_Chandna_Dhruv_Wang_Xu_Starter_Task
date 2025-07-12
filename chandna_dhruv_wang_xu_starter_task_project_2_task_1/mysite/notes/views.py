from django.shortcuts import render, redirect
from .models import Article
from .forms import PDFUploadForm

# Create your views here.
def article_list(request):
    articles = Article.objects.all()
    return render(request, "notes/article_list.html", {"articles": articles})

def upload_pdf_view(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("view_pdf", article_id=article.id)
    else:
        form = PDFUploadForm()
    return render(request, "notes/upload_pdf.html", {"form": form})

def view_pdf(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, "notes/view_pdf.html", {"article": article})
    
