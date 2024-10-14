from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='feedback_attachments/', blank=True, null=True)

    def __str__(self):
        return self.subject