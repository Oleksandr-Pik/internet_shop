import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmation_codes")
    code = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"ConfirmationCode(user={self.user.email}, code={self.code})"
    
    @classmethod
    def process_code(cls, code: str) -> bool:
        try:
            confirmation_code = cls.objects.get(code=code)
            user = confirmation_code.user
            user.is_active = True
            user.save()
            confirmation_code.delete()
            return user
        except cls.DoesNotExist:
            return None

    def save(self, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        self.user.confirmation_codes.all().delete()
        return super().save(**kwargs)
