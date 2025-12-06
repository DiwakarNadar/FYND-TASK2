from django.db import models

class Submission(models.Model):
    user_rating = models.IntegerField()
    user_review = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)
    ai_actions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_rating} - {self.user_review[:30]}"
