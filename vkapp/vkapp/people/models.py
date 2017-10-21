from django.db import models


class Client(models.Model):
    vk_id_ref = models.IntegerField()
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    is_deleted = models.BinaryField(default=False)
    description = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)

    def __str__(self):
        return(self.name)
