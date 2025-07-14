from django.db import models

class Article(models.Model):

    def __str__(self):
        return f"Title: {self.title} | PDF URL: {self.pdf_url}"
    
    title = models.CharField(max_length=200)
    pdf_url = models.URLField(blank=True, null=True)

class Annotation(models.Model):
    
    def __str__(self):
        return f"Annotation {self.id} on Article {self.article_id} - Type: {self.annotation_type} at Page {self.page}"
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='annotations')
    annotation_type = models.CharField(max_length=20, choices=[('highlight', 'Highlight'), ('underline', 'Underline')])
    page = models.IntegerField()
    left = models.FloatField()
    top = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    
    def __str__(self):
        return f"Note {self.id} on Article {self.article_id} - Title: {self.title}"
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='notes')
    annotation = models.OneToOneField(Annotation, on_delete=models.CASCADE, related_name='note', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)