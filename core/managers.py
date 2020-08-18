from django.db import models
from .models import Candidate


class TestManager(models.Manager):

    def get_test(self):
        email = self.request.session["email"]
        candidate = Candidate.objects.get(email=email)
        return self.model.objects.get(test_name=candidate.test_name)
