import os
import shutil
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

def student_images_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.student_rollno}.{ext}"
    return os.path.join('student_images', filename)

class Student(models.Model):   
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    student_rollno = models.CharField(max_length=20, unique=True)
    student_image = models.ImageField(upload_to='dataset/', null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.student_name} ({self.student_rollno})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    student_name = models.CharField(max_length=100, null=True, blank=True)
    student_rollno = models.CharField(max_length=20, null=True, blank=True)
    student_image = models.ImageField(upload_to="attendance_images/", null=True, blank=True)
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])
    date = models.DateField(default=timezone.now)
    time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student_name} - {self.date} - {self.status}"

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os
import shutil

@receiver(post_save, sender=Student)
def copy_image_to_dataset(sender, instance, **kwargs):
    if instance.student_image:
        dataset_folder = os.path.join(settings.MEDIA_ROOT, 'dataset')
        os.makedirs(dataset_folder, exist_ok=True)

        ext = 'jpg'  # force jpg format
        dest_path = os.path.join(dataset_folder, f"{instance.student_rollno}.{ext}")
        src_path = os.path.abspath(instance.student_image.path)
        dest_path_abs = os.path.abspath(dest_path)

        # Skip copying if source and destination are the same
        if src_path != dest_path_abs:
            try:
                # Convert image to JPG if needed
                from PIL import Image
                img = Image.open(src_path).convert('RGB')
                img.save(dest_path_abs, 'JPEG')
                print(f"✅ Dataset image saved: {dest_path_abs}")
            except Exception as e:
                print(f"⚠️ Could not save image: {e}")
        else:
            print(f"ℹ️ Image already in dataset: {dest_path_abs}")

@receiver(post_delete, sender=Student)
def delete_dataset_image(sender, instance, **kwargs):
    if instance.student_image:
        dataset_folder = os.path.join(settings.MEDIA_ROOT, 'dataset')
        file_path = os.path.join(dataset_folder, f"{instance.student_rollno}.jpg")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️ Deleted dataset image: {file_path}")
