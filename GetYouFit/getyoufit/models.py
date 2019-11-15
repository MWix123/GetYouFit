# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Post(models.Model):
	text = models.TextField()
	textarea = models.TextField()

	def publish(self):
		self.save()

	def __str__(self):
		return self.textarea
