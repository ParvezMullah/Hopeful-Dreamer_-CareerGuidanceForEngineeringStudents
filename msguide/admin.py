from django.contrib import admin
from msguide.models import (
    UserProfile,
    University
)
# Register your models here.


class UniversityAdmin(admin.ModelAdmin):
    fieldsets = [
        ('University Details', {'fields': ['University', 'country']}),
        ('GRE Scores', {'fields': [
         'gre_verbal', 'gre_writing', 'gre_quantitative', 'gre_percentile']}),
        ('TOEFL', {'fields': [
         'toefl', ]}),
        ('University Status', {'fields': ['overall_rating', 'grade', ]}),
    ]
    # date_hierarchy = 'date_found_or_lost'   #archieve or for that specific hierarchy.

    class Meta:
        model = University


admin.site.register(University, UniversityAdmin)
admin.site.register(UserProfile)
admin.site.site_header = 'MS Guidance Admininstration'
