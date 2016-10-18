from django.contrib import admin
from .models import Moneydonate, MoneydonateAmount


class MoneydonateAmountInlineAdmin(admin.TabularInline):
    model = MoneydonateAmount
    extra = 0
    min_num = 0
