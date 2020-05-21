from django.contrib import admin
from main.models import Document, Rule, Profile

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'file',
        'content_type',
    ]
    
@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]