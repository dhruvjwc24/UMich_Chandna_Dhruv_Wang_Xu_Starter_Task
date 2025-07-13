# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Article, Annotation, Note
from .forms import PDFUploadForm
import json

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
    article = get_object_or_404(Article, pk=article_id)
    annotations = article.annotations.all()
    notes = article.notes.all().order_by("annotation__page", "annotation__top")
    return render(request, "notes/view_pdf.html", {
        "article": article,
        "annotations": annotations,
        "notes": notes
    })

def save_annotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        annotation = Annotation.objects.create(
            article_id=data['article_id'],
            annotation_type=data['type'],
            page=data['page'],
            left=data['left'],
            top=data['top'],
            width=data['width'],
            height=data['height']
        )
        note = Note.objects.create(
            article_id=data['article_id'],
            annotation=annotation,
            title="",
            body=""
        )
        return JsonResponse({"annotation_id": annotation.id, "note_id": note.id})

def update_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = get_object_or_404(Note, pk=data['note_id'])
        note.title = data.get('title', note.title)
        note.body = data.get('body', note.body)
        note.save()
        return JsonResponse({"status": "updated"})

def delete_annotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        annotation = get_object_or_404(Annotation, pk=data['annotation_id'])
        annotation.delete()
        return JsonResponse({"status": "deleted"})