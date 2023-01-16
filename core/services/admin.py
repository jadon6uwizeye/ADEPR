import json
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Offering)
admin.site.register(OfferingCategory)
admin.site.register(DocumentRequest)
admin.site.register(Document)


class MemberAdmin(admin.ModelAdmin):


    def changelist_view(self, request, extra_context=None): 
        chart_data = (
            Member.objects.filter(church_members__isnull=True).distinct().annotate(
                date=TruncDay("created_on__date"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"),
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Member)
