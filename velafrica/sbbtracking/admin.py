# -*- coding: utf-8 -*-
from django import forms
from django import template
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType, EmailLog, VeloType
from import_export import resources
from import_export.admin import ImportExportMixin


class TrackingEventInline(admin.TabularInline):
    model = TrackingEvent
    extra = 0


class EmailLogInline(admin.TabularInline):
    model = EmailLog
    fields = ('datetime', 'receiver', 'subject', 'message')
    readonly_fields = ('datetime', 'receiver', 'subject', 'message')
    extra = 0

    # do not allow users to create new email logs themselves
    def has_add_permission(self, request):
        return False

class VeloTypeAdmin(SimpleHistoryAdmin):
    model = VeloType

class TrackingResource(resources.ModelResource):
    """
    Define the Tracking resource for import / export.
    """

    class Meta:
        model = Tracking
        import_id_fields = ('tracking_no',)
        fields = ('first_name', 'last_name', 'email', 'tracking_no', 'number_of_velos', 'last_event__event_type__name', 'velo_type__name')

class TrackingAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = TrackingResource
    list_display = ('tracking_no', 'first_name', 'last_name', 'number_of_velos', 'velo_type', 'get_last_update', 'last_event', 'complete', 'container')
    list_filter = ['last_event__event_type', 'velo_type', 'complete']
    inlines = [TrackingEventInline, EmailLogInline]
    search_fields = ['tracking_no', 'first_name', 'last_name']
    readonly_fields = ['last_event']

    actions = ['add_event',]

    class AddEventForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        event_type = forms.ModelChoiceField(TrackingEventType.objects)

    def add_event(self, request, queryset):
        """
        Admin action to add events to trackings.
        """
        form = None

        if 'apply' in request.POST:
            form = self.AddEventForm(request.POST)

            if form.is_valid():
                event_type = form.cleaned_data['event_type']

                count = 0
                for t in queryset:
                    t.id
                    tracking_event = TrackingEvent(
                        event_type=event_type,
                        tracking=t)
                    tracking_event.save()
                    count += 1

                plural = ''
                if count != 1:
                    plural = 's'

                self.message_user(request, "Successfully added event %s to %d tracking%s." % (event_type, count, plural))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AddEventForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render_to_response(
            'admin/add_event.html', 
            {'trackings': queryset, 'tag_form': form },
            context_instance=template.RequestContext(request)
        )
    add_event.short_description = "Add event to trackings"    


class TrackingEventTypeAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description', 'send_email', 'complete_tracking')


admin.site.register(VeloType, VeloTypeAdmin)
admin.site.register(Tracking, TrackingAdmin)
admin.site.register(TrackingEventType, TrackingEventTypeAdmin)
