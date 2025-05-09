from django.contrib import admin
from .models import Category, Customer, Product, UserProfile
from django.contrib.auth.models import User

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = UserProfile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)