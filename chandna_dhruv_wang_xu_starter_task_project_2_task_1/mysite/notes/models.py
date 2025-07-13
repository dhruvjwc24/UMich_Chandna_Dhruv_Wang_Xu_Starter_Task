from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Annotation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='annotations')
    annotation_type = models.CharField(max_length=20, choices=[('highlight', 'Highlight'), ('underline', 'Underline')])
    page = models.IntegerField()
    left = models.FloatField()
    top = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='notes')
    annotation = models.OneToOneField(Annotation, on_delete=models.CASCADE, related_name='note', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)