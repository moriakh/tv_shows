from django.db import models

# Create your models here.
class Shows(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    desc = models.TextField(default="some tv show")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Networks(models.Model):
    name = models.CharField(max_length=255)
    shows = models.ForeignKey(Shows, related_name="networks", on_delete = models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)