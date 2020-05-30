from django.contrib import admin
from main.models import Document, Case, Rule, Profile

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'file',
        'originalName',
        'case',
        'isFinished',
    ]

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        'name',
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