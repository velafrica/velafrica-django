# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords