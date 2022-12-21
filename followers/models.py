from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Follower model, related to the 'owner' object.
    'owner' is a User instance.
    'unique_together' makes sure a user can't duplicate follows.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            '-created_at'
        ]
        unique_together = [
            'owner', 'followed'
        ]

    def __str__(self):
        f'{self.owner}, {self.followed}'
