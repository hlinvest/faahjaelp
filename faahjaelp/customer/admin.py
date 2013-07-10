from django.contrib import admin
from customer.models import Comment, Customer

class SLugAdmin(admin.ModelAdmin):
    prepopulate_fields={'slug':('username',)}
    list_display=('username','email','isWorker')
    search_fields=('username','email')
    
admin.site.register(Comment)
admin.site.register(Customer)
