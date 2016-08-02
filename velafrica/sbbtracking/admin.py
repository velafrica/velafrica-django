# -*- coding: utf-8 -*-
import inspect
from django_object_actions import DjangoObjectActions
from django import forms
from django import template
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType, EmailLog, VeloType
from import_export import resources
from import_export.admin import ImportExportMixin


def create_trackingevent_form(tracking):
    """
    """
    class TrackingEventForm(forms.ModelForm):
        """
        Form for Tracking Event Inline
        """

        def clean(self):
            """
            May not be needed anymore, since event type choices are limited when creating new event.
            """
            next_eventtype = self.cleaned_data['event_type']
            tracking = self.cleaned_data['tracking']
            # get last event, this also ensures last_event gets updated everytime the change form for TrackingEvent is loaded
            last_eventtype = tracking.set_last_event()

            if last_eventtype:
                last_eventtype = last_eventtype.event_type

            pk = self.instance.pk
            insert = pk == None
            # check if the event is updated or newly created
            if insert:
                if next_eventtype.required_previous_event == last_eventtype:
                    pass
                else:
                    raise forms.ValidationError('"{}" requires "{}" as last event, "{}" found. Possible next events: {}'.format(
                        next_eventtype, 
                        next_eventtype.required_previous_event, 
                        last_eventtype,
                        '"%s" ' % ', '.join(map(str, [x.name for x in  tracking.next_tracking_eventtype_options()]))
                        )
                    )
            else:
                pass
            return self.cleaned_data

        def __init__(self, *args, **kwargs):
            # You can use the outer function's 'tracking' here
            self.parent_object = tracking

            super(TrackingEventForm, self).__init__(*args, **kwargs)
            self.fields['event_type'].queryset = tracking.next_tracking_eventtype_options()
            #self.fields['event_type'].limit_choices_to = tracking.next_tracking_eventtype_options()

    return TrackingEventForm


class TrackingEventInline(admin.TabularInline):
    #form = MyForm
    #formset = MyFormSet

    model = TrackingEvent
    extra = 0

    #readonly_fields = ['datetime', 'event_type', 'note']

    def has_add_permission(self, request):
        return False

    

class AddTrackingEventInline(admin.TabularInline):
    model = TrackingEvent
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def queryset(self, request): 
        return super(AddTrackingEventInline, self).queryset(request).none()

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.form = create_trackingevent_form(obj)
        return super(AddTrackingEventInline, self).get_formset(request, obj, **kwargs)


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
        fields = ('first_name', 'last_name', 'email', 'tracking_no', 'last_event__event_type__name', 'velo_type__name')

class TrackingAdmin(DjangoObjectActions, ImportExportMixin, SimpleHistoryAdmin):
    resource_class = TrackingResource
    list_display = ('tracking_no', 'first_name', 'last_name', 'velo_type', 'get_last_update', 'last_event', 'complete', 'container', 'note')
    list_filter = ['last_event__event_type', 'velo_type', 'complete']
    inlines = [TrackingEventInline, AddTrackingEventInline, EmailLogInline]
    search_fields = ['tracking_no', 'first_name', 'last_name', 'email']
    readonly_fields = ['last_event']

    actions = ['add_event',]
    change_actions = ['fix_last_event']

    class AddEventForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        event_type = forms.ModelChoiceField(TrackingEventType.objects)

    def fix_last_event(self, request, obj):
        """
        """
        event = obj.set_last_event()
        if event:
            self.message_user(request, "Letzten Event erfolgreich aktualisiert zu {}.".format(event))
    fix_last_event.label = "Letzter Event korrigieren"


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
