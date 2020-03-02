from django.contrib import admin
from main.models import Document, UserProfile, Rule, Profile

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'file',
        'author',
        'content_type',
    ]
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'is_lawyer',
        'is_curator',
    ]
    
@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author'
    ]
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author'
    ]