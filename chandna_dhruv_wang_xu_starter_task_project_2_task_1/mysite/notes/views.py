# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Article, Annotation, Note
from .forms import PDFUploadForm
import json

from transformers import pipeline
model = pipeline("summarization", model="facebook/bart-large-cnn")

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
  # 👇 Add this for debugging
    print(f"[DEBUG] Article ID: {article.id}")
    print(f"[DEBUG] Title: {article.title}")
    print(f"[DEBUG] PDF URL: {article.pdf_url}")    
    
    annotations_qs = Annotation.objects.filter(article=article).select_related('note')
    annotations = []
    for a in annotations_qs:
        annotations.append({
            "id": a.id,
            "article_id": a.article_id,
            "annotation_type": a.annotation_type,
            "page": a.page,
            "left": a.left,
            "top": a.top,
            "width": a.width,
            "height": a.height,
            "note": {
                "id": a.note.id if hasattr(a, 'note') and a.note else None,
                "title": a.note.title if hasattr(a, 'note') and a.note else "",
                "body": a.note.body if hasattr(a, 'note') and a.note else "",
            }
        })
    
    notes = article.notes.all().order_by("annotation__page", "annotation__top")
    return render(request, "notes/view_pdf.html", {
        "article": article,
        "annotations": annotations,
        "notes": notes
    })
    
def delete_note_and_annotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        annotation = get_object_or_404(Annotation, pk=data['annotation_id'])
        print(annotation.id)
        try:
            note = annotation.note
        except Note.DoesNotExist:
            note = None
        annotation.delete()
        note.delete() if note else None
        return JsonResponse({"status": "deleted"})
    
def update_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = get_object_or_404(Note, pk=data['note_id'])
        note.title = data.get('title', note.title)
        note.body = data.get('body', note.body)
        note.save()
        return JsonResponse({"status": "success"})
    
def suggest_note(request):
    if request.method == "POST":
        suggestedTitle = "Title (optional)"
        suggestedBody = "Write your note here..."
        
        data = json.loads(request.body)
        selectedText = data.get('selectedText', '').strip()
        selectedTextLength = selectedText.count(" ") + 2 if selectedText else 0
        
        MIN_LENGTH = int(selectedTextLength * 0.25)
        MAX_LENGTH = int(selectedTextLength * 0.75)
        
        response = model(selectedText, max_length=MAX_LENGTH, min_length=MIN_LENGTH, do_sample=False)[0]["summary_text"]
        suggestedBody = response if response else suggestedBody
        
        return JsonResponse({"status": "success", "suggestedTitle": suggestedTitle, "suggestedBody": response})
        
        
        
    
@csrf_exempt
def save_annotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(f"[DEBUG] ANNOATATION DATA: {data}")
        annotation = Annotation.objects.create(
            id=data['annotation_id'],
            article_id=data['article_id'],
            annotation_type=data['type'],
            page=data['page'],
            left=data['left'],
            top=data['top'],
            width=data['width'],
            height=data['height']
        )
        
        annotation.save()
        
        return JsonResponse({"status": "success", "annotation_id": annotation.id})
    
@csrf_exempt
def save_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"[DEBUG] NOTE DATA: {data}")
        
        if(data["title"] == "" and data["content"] == ""):
            return JsonResponse({'status': 'success', 'message': 'Empty note created'})
                
        if data['note_id'] != "null":
            print(f"[DEBUG] NOTE ID FOund - UPDATE: {data}")

            note = get_object_or_404(Note, pk=data['note_id'])

            note.title = data["title"]
            note.body = data["content"]
        else:
            print(f"[DEBUG] NOTE ID NOTE FOUND - CREATE: {data}")

            note = Note.objects.create(
                article_id=data['article_id'],
                annotation_id=data['annotation_id'],
                title=data["title"],
                body=data["content"]
            )
     
        note.save()
            
        return JsonResponse({'status': 'success', 'note_id': note.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)