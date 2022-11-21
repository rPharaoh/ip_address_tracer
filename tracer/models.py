import secrets

from django.db import models


class UserData(models.Model):
    ip_address = models.TextField(null=True)
    user_agent = models.TextField(null=True)
    address = models.TextField(null=True)
    location = models.TextField(null=True)
    map = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    DEFAULT = 'default'
    OLD = 'old'
    CHOICES = (
        ('Default', DEFAULT),
        ('old', OLD),
    )
    status = models.CharField(max_length=50, choices=CHOICES, default=DEFAULT)

    def save(self, **kwargs):
        if not self.pk:
            self.id = secrets.randbits(32)
        super(UserData, self).save(**kwargs)
