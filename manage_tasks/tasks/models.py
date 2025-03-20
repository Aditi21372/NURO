from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField()
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def clean(self):
        if self.priority < 1 or self.priority > 5:
            raise ValidationError('Priority must be between 1 and 5.')


    def __str__(self):
        return self.title
