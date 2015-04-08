"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


"""
Custom user form to extend the normal user model and add key field
"""
class SecureUser(AbstractBaseUser):
	username = models.CharField(max_length=40, unique=True, db_index=True)
	email = models.EmailField(max_length=254, unique=True)
	key = models.CharField(max_length=16)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def set_key(self, value):
		self.key = value

	def get_key(self):
		return self.key