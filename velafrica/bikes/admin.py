# -*- coding: utf-8 -*-
import datetime
import io
import os
import sys

from django.contrib.contenttypes.models import ContentType
from django.conf.urls import url
from django.contrib.admin import helpers
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.forms import all_valid
from django.http import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin

from velafrica.bikes.models import Bike
from velafrica.core.settings import PROJECT_DIR

from reportlab.lib.utils import simpleSplit

from pdfrw import PdfReader

def get_formsets(model, request, obj=None):
    return [f for f, _ in model.get_formsets_with_inlines(request, obj)]


class BikeResource(resources.ModelResource):
    class Meta:
        model = Bike


# Filters out all A+ Bikes which are still for sale
class APlusForSaleListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'A+ for sale'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'a_plus_for_sale'

    def lookups(self, request, model_admin):
        return (  # most return more than one
            ('1', 'YES'),
            ('0', '-')
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(container__exact=None, a_plus__exact=True)


# TODO: show details fields only when A+ is selected
class BikeAdmin(ImportExportMixin, DjangoObjectActions, admin.ModelAdmin):
    fontsize = 12  # pdf font size
    labels = {key: Bike._meta.get_field(key).verbose_name for key in Bike.plotable}  # labels for pdf

    resource_class = BikeResource  # import export

    list_display = ['number', 'type', 'brand', 'a_plus', 'for_sale', 'container', 'warehouse']
    search_fields = ['id', 'type', 'brand', 'a_plus', 'warehouse']
    list_filter = [APlusForSaleListFilter, 'a_plus', 'type', 'container', 'warehouse', ('date', DateRangeFilter)]

    # "for_sale" a boolean column in the list-view
    def for_sale(self, obj):
        return obj.container is None

    for_sale.short_description = "For sale"
    for_sale.admin_order_field = 'container'
    for_sale.boolean = True

    book_bike_exclude = ['number', 'type', 'visa', 'date', 'a_plus', 'brand', 'bike_model', 'gearing',
                         'drivetrain', 'type_of_brake', 'brake', 'colour', 'size', 'suspension',
                         'rear_suspension', 'extraordinary', 'image']

    # actions on selected elements
    actions = ["plot_to_pdf", "book_bikes_action"]

    #
    #  Detail view
    #

    fieldsets = (
        (None, {
            'fields': ('id', 'number', 'type', 'visa', 'date', 'warehouse')
        }),
        ('A+',  # Details ?
         {
             'fields': ('a_plus', 'brand', 'bike_model', 'gearing',  # 'crankset',
                        'drivetrain', 'type_of_brake', 'brake', 'colour', 'size',
                        'suspension', 'rear_suspension', 'extraordinary', 'image'
                        ),
         }
         ),
        ('Container',
         {
             'fields': ['container']
         }
         ),
    )

    readonly_fields = ['id']

    fieldset_book = [
        (None, {
            'fields': ('container', 'warehouse'),
        })
    ]

    list_max_show_all = 1000
    list_per_page = 100

    # PDF-PLOT
    # TODO: language-labels
    def draw_pdf_page(self, c, bike):
        # Header - Title and Logo
        c.setFont("Helvetica", 32)
        c.drawString(x=40, y=510, text="A+ Bike")
        c.drawImage(
            os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg'),
            x=657.5, y=471, width=2466 / 15, height=1565 / 15
        )

        # Bike
        c.setFont("Helvetica", self.fontsize)

        y = 450 - self.fontsize  # origin of coordinates is bottom left
        for key in Bike.plotable:
            if bike.__getattribute__(key):  # if not blank
                # label
                c.drawString(40, y, self.labels[key])

                # breaks lines if too long
                # and then draw line by line
                for line in simpleSplit(text=str(bike.__getattribute__(key)),
                                        fontName=c._fontname,
                                        fontSize=c._fontsize,
                                        maxWidth=130):
                    c.drawString(175, y, line)
                    y -= 14
                # add spacing between two rows
                y -= 12

        # plot image of bike
        if bike.image:
            w = 480  # fixed width
            h = bike.image.height / bike.image.width * w  # keep ratio
            c.drawImage(
                bike.image.url,
                x=321.9, y=450 - h, width=w, height=h
            )

        # End Page
        c.showPage()

    def plot_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buf, pagesize=landscape(A4))  # W, H = landscape(A4)  # 841.9, 595.27

        # Add Preface (page by page)
        for page in PdfReader(PROJECT_DIR + "/media/APlusPreface.pdf").pages:
            p.doForm(makerl(p, pagexobj(page)))
            p.showPage()

        # create a pdf page for each bike
        for bike in queryset:
            self.draw_pdf_page(p, bike)

        # Close the PDF object cleanly
        p.save()
        buf.seek(0)

        # define HTT-Response
        response = StreamingHttpResponse(buf, content_type="application/pdf")  # set type to PDF
        # name the document and download it
        filename = "{} A-Plus bikes for sale.pdf".format(
            datetime.datetime.now().strftime('%Y-%m-%d')
        )
        response['Content-Disposition'] = "attachment;filename={}".format(filename)
        return response

    plot_to_pdf.short_description = "Als PDF Drucken"

    def get_urls(self):
        return [
            url(
                r'^book/(?P<object_ids>[\w,\.\-]+)/$',
                self.book_bikes_view,
                name='bikes_bike_book'
            ),
        ] + super(BikeAdmin, self).get_urls()

    #
    # Book mutiple bikes at once
    # Source code from django.massadmin (2010)
    # Credits to Stanislaw Adaszewski
    #
    # A bit change adjusted...
    #
    def book_bikes_view(self, request, object_ids, extra_context=None):
        global new_object
        opts = self.model._meta
        general_error = None

        queryset = self.get_queryset(request)

        _object_ids = object_ids.split(',')
        object_id = _object_ids[0]

        try:
            obj = queryset.get(pk=unquote(object_id))
        except self.model.DoesNotExist:
            obj = None

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                '%(name)s object with primary key %(key)r does not exist.' % {
                    'name': force_text(opts.verbose_name),
                    'key': escape(object_id)
                }
            )

        ModelForm = self.get_form(request, obj)
        formsets = []
        errors, errors_list = None, None
        mass_changes_fields = request.POST.getlist("_mass_change")  # ["container", "warehouse"]
        if request.method == 'POST':
            # commit only when all forms are valid
            try:
                with transaction.atomic():
                    objects_count = 0
                    changed_count = 0
                    objects = queryset.filter(pk__in=_object_ids)
                    for obj in objects:
                        objects_count += 1
                        form = ModelForm(request.POST, request.FILES, instance=obj)

                        exclude = [
                            fieldname
                            for fieldname, field in list(form.fields.items())
                            if fieldname not in mass_changes_fields
                        ]

                        for exclude_fieldname in exclude:
                            del form.fields[exclude_fieldname]

                        new_object = self.save_form(request, form, change=True) if form.is_valid() else obj

                        prefixes = {}
                        for FormSet in get_formsets(self, request, new_object):
                            prefix = FormSet.get_default_prefix()
                            prefixes[prefix] = prefixes.get(prefix, 0) + 1
                            if prefixes[prefix] != 1:
                                prefix = "%s-%s" % (prefix, prefixes[prefix])
                            if prefix in mass_changes_fields:
                                formsets.append(
                                    FormSet(request.POST, request.FILES, instance=new_object, prefix=prefix)
                                )

                        if all_valid(formsets) and form.is_valid():
                            self.save_model(request, new_object, form, change=True)
                            form.save_m2m()
                            for formset in formsets:
                                self.save_formset(request, form, formset, change=True)

                            change_message = self.construct_change_message(request, form, formsets)
                            self.log_change(request, new_object, change_message)
                            changed_count += 1

                    if changed_count == objects_count:
                        return self.response_change(request, new_object)
                    else:
                        errors = form.errors
                        errors_list = helpers.AdminErrorList(form, formsets)
                        # Raise error for rollback transaction in atomic block
                        raise ValidationError("Not all forms is correct")
            except:
                general_error = sys.exc_info()[1]

        form = ModelForm(instance=obj)
        form._errors = errors
        prefixes = {}
        for FormSet in get_formsets(self, request, obj):
            prefix = FormSet.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset = FormSet(instance=obj, prefix=prefix)
            formsets.append(formset)

        adminForm = helpers.AdminForm(
            form=form,
            fieldsets=self.fieldset_book,
            prepopulated_fields=self.prepopulated_fields,
            readonly_fields=self.get_readonly_fields(request, obj),
            model_admin=self
        )

        request.current_app = self.admin_site.name

        return render(
            request=request,
            template_name="bikes/change_multiple_form.html",
            context={
                'title': 'Book multiple %s' % force_text(opts.verbose_name),
                'adminform': adminForm,
                'object_id': object_id,
                'original': obj,
                'unique_fields': [  # We don't want the user trying to mass change unique fields!
                    field.name
                    for field in opts.get_fields()
                    if field.unique
                ],
                'exclude_fields': self.book_bike_exclude,
                'is_popup': '_popup' in request.GET or '_popup' in request.POST,
                'media': mark_safe(self.media + adminForm.media),
                'errors': errors_list,
                'general_error': general_error,
                'app_label': opts.app_label,
                'object_ids': object_ids,
                'mass_changes_fields': mass_changes_fields,
                'add': False,
                'change': True,
                'has_add_permission': self.has_add_permission(request),
                'has_change_permission': self.has_change_permission(request, obj),
                'has_delete_permission': self.has_delete_permission(request, obj),
                'has_file_field': True,
                'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
                'form_url': mark_safe(''),
                'opts': opts,
                'content_type_id': ContentType.objects.get_for_model(self.model).id,
                'save_as': self.save_as,
                'save_on_top': self.save_on_top,
            },
        )

    def book_bikes_action(self, request, queryset):
        return HttpResponseRedirect(
            add_preserved_filters(
                context={
                    'preserved_filters': self.get_preserved_filters(request),
                    'opts': queryset.model._meta
                },
                url=reverse(
                    "admin:bikes_bike_book",
                    kwargs={
                        "object_ids": ",".join(
                            str(pk)
                            for pk in queryset.values_list('pk', flat=True)
                        )
                    }
                )
            )
        )

    book_bikes_action.short_description = "Velos buchen / verschieben"


admin.site.register(Bike, BikeAdmin)
