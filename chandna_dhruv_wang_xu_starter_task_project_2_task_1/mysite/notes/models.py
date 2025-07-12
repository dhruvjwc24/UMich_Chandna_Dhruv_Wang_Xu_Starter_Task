from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    pdf_url = models.URLField("PDF_URL", blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.title

class Note(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on {self.article.title} ({self.created_at.date()})"