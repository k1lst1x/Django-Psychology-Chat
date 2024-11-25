from django.db import models
import os

def methodology_file_path(instance, filename):
    return os.path.join('static', 'methodologies', filename)

class Methodology(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название методики")
    instructions = models.CharField(max_length=512, verbose_name="Инструкции")
    file = models.FileField(upload_to=methodology_file_path, verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Методика"
        verbose_name_plural = "Методики"

def report_file_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'reports', filename)

class Report(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('kz', 'Казахский'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    military_number = models.CharField(max_length=50, verbose_name="Номер военнослужащего")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name="Язык")
    file = models.FileField(upload_to=report_file_path, verbose_name="Файл отчета", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    def __str__(self):
        return f"{self.full_name} - {self.get_language_display()}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
