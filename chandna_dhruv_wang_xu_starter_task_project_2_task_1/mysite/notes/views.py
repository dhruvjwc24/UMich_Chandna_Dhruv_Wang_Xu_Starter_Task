# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
  # 👇 Add this for debugging
    print(f"[DEBUG] Article ID: {article.id}")
    print(f"[DEBUG] Title: {article.title}")
    print(f"[DEBUG] PDF URL: {article.pdf_url}")    
    annotations = list(Annotation.objects.filter(article=article).values())
    notes = article.notes.all().order_by("annotation__page", "annotation__top")
    return render(request, "notes/view_pdf.html", {
        "article": article,
        "annotations": annotations,
        "notes": notes
    })
    
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
                
        note = Note.objects.create(
            article_id=data['article_id'],
            annotation_id=data['annotation_id'],
            title=data["title"],
            body=data["content"]
        )
        
        note.save()
            
        return JsonResponse({'status': 'success', 'note_id': note.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def save_note_old(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"DATA: {data}")
        annotation_id = data.get('annotation_id')
        title = data.get('title', '')
        content = data.get('content', '')
        note_id = data.get('note_id')
        print(f"[DEBUG] note_id: {note_id}")
        print(f"[DEBUG] annotation_id: {annotation_id}")
        
        try:
            annotation = Annotation.objects.get(id=annotation_id)
            print(f"[DEBUG] Annotation Object: {annotation.id}")
            
        except(ValueError, KeyError, Annotation.DoesNotExist) as e:
            print(f"[DEBUG] Annotation Object Exception")
            print(f"[DEBUG] Exception Type: {type(e).__name__}")
            print(f"[DEBUG] Exception Message: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=404)

        if note_id:
            note = Note.objects.get(id=note_id)
            note.title = title
            note.content = content
        else:
            print(f"[DEBUG] note_id else: {note_id}")
            note = Note(annotation=annotation, title=title, content=content)

        note.save()

        return JsonResponse({'status': 'success', 'note_id': note.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)