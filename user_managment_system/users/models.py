from django.db import models
import uuid

# Create your models here.
class UsersData(models.Model):
    user_id = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    user_age = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    email = models.CharField(max_length=255)
    web = models.URLField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["first_name"], name="first_name_idx"),
        ]
        db_table = 'user_data'
