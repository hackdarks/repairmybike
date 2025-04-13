# data_import/models.py
from django.db import models

class ExcelImport(models.Model):
    file = models.FileField(upload_to='imports/')
    imported_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"File imported at {self.imported_at}"
