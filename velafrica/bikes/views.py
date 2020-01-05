# -*- coding: utf-8 -*-
import datetime
import io
import os
import sys

from dal import autocomplete
from django.contrib.admin import helpers
from django.contrib.admin.utils import unquote
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.forms import all_valid
from django.http import Http404
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import ListView
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from velafrica.bikes.models import Bike, BikeCategory
from velafrica.core.settings import PROJECT_DIR
from velafrica.velafrica_sud.models import Container


class BikePDFView(View):
    fontsize = 12  # pdf font size

    # fields used from plot_to_pdf
    fields = {
        "number": "No.",
        "category": "Type",
        "brand": "Brand",
        "bike_model": "Model",
        "gearing": "Group of components",
        "drivetrain": "Drivetrain",
        "brake": "Brake",
        "colour": "Colour",
        "size": "Size",
        "suspension": "Suspension",
        "rear_suspension": "Rear suspension"
    }

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
        for key, label in self.fields.items():
            if bike.__getattribute__(key):  # if not blank
                # label
                c.drawString(40, y, label)

                # breaks lines if too long
                # and then draw line by line
                for line in simpleSplit(text=str(bike.__getattribute__(key)),
                                        fontName=c._fontname,
                                        fontSize=c._fontsize,
                                        maxWidth=130):
                    c.drawString(175, y, line)
                    y -= 15
                # add spacing between two rows
                y -= 6

        if bike.extraordinary and bike.extraordinary != "":
            c.drawString(40, y, "Extraordinary:")
            y -= 16
            for line in simpleSplit(text=str(bike.extraordinary),
                                    fontName=c._fontname,
                                    fontSize=c._fontsize,
                                    maxWidth=255):
                c.drawString(50, y, line)
                y -= 14

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

    def get(self, request, key, *args, **kwargs):
        # check permission
        if not request.user.has_perm("{}.{}_{}".format("bikes", "change", "Bike")):
            raise PermissionDenied

        if key == 'for_sale':
            queryset = Bike.objects.filter(container__isnull=True, a_plus__exact=True)
        else:
            queryset = get_list_or_404(Bike, pk__in=pks.split(','))

        # Create a file-like buffer to receive PDF data.
        buf = io.BytesIO()

        a_plus_for_sale = "a_plus_for_sale" in request.GET
        container = request.GET['container'] if 'container' in request.GET else None

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buf, pagesize=landscape(A4))  # W, H = landscape(A4)  # 841.9, 595.27

        if a_plus_for_sale:
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

        # name the document
        name = "{} bikes".format(
            datetime.datetime.now().strftime('%Y-%m-%d')
        )
        if container:
            name = "bikes sold {}".format(
                get_object_or_404(Container, pk=container)
            )
        elif a_plus_for_sale:
            name = "{} A-Plus bikes for sale".format(
                datetime.datetime.now().strftime('%Y-%m-%d')
            )

        # and download it
        response['Content-Disposition'] = "attachment;filename={}.pdf".format(name)
        return response


def book_bikes_view(model_admin, request, object_ids, extra_context=None):
    fieldsets = [
        (None, {
            'fields': ('container', 'warehouse'),
        })
    ]

    new_object = None
    opts = model_admin.model._meta
    general_error = None

    queryset = model_admin.get_queryset(request)

    _object_ids = object_ids.split(',')
    object_id = _object_ids[0]

    try:
        obj = queryset.get(pk=unquote(object_id))
    except model_admin.model.DoesNotExist:
        obj = None

    if not model_admin.has_change_permission(request, obj):
        raise PermissionDenied

    if obj is None:
        raise Http404(
            '%(name)s object with primary key %(key)r does not exist.' % {
                'name': force_text(opts.verbose_name),
                'key': escape(object_id)
            }
        )

    ModelForm = model_admin.get_form(request, obj)
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

                    new_object = model_admin.save_form(request, form, change=True) if form.is_valid() else obj

                    prefixes = {}
                    for FormSet, _ in model_admin.get_formsets_with_inlines(request, new_object):
                        prefix = FormSet.get_default_prefix()
                        prefixes[prefix] = prefixes.get(prefix, 0) + 1
                        if prefixes[prefix] != 1:
                            prefix = "%s-%s" % (prefix, prefixes[prefix])
                        if prefix in mass_changes_fields:
                            formsets.append(
                                FormSet(request.POST, request.FILES, instance=new_object, prefix=prefix)
                            )

                    if all_valid(formsets) and form.is_valid():
                        model_admin.save_model(request, new_object, form, change=True)
                        form.save_m2m()
                        for formset in formsets:
                            model_admin.save_formset(request, form, formset, change=True)

                        change_message = model_admin.construct_change_message(request, form, formsets)
                        model_admin.log_change(request, new_object, change_message)
                        changed_count += 1

                if changed_count == objects_count:
                    return model_admin.response_change(request, new_object)
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
    for FormSet, _ in model_admin.get_formsets_with_inlines(request, new_object):
        prefix = FormSet.get_default_prefix()
        prefixes[prefix] = prefixes.get(prefix, 0) + 1
        if prefixes[prefix] != 1:
            prefix = "%s-%s" % (prefix, prefixes[prefix])
        formset = FormSet(instance=obj, prefix=prefix)
        formsets.append(formset)

    adminForm = helpers.AdminForm(
        form=form,
        fieldsets=fieldsets,
        prepopulated_fields=model_admin.prepopulated_fields,
        readonly_fields=model_admin.get_readonly_fields(request, obj),
        model_admin=model_admin
    )

    request.current_app = model_admin.admin_site.name

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
            'exclude_fields': [],
            'is_popup': '_popup' in request.GET or '_popup' in request.POST,
            'media': mark_safe(model_admin.media + adminForm.media),
            'errors': errors_list,
            'general_error': general_error,
            'app_label': opts.app_label,
            'object_ids': object_ids,
            'mass_changes_fields': mass_changes_fields,
            'add': False,
            'change': True,
            'has_add_permission': model_admin.has_add_permission(request),
            'has_change_permission': model_admin.has_change_permission(request, obj),
            'has_delete_permission': model_admin.has_delete_permission(request, obj),
            'has_file_field': True,
            'has_absolute_url': hasattr(model_admin.model, 'get_absolute_url'),
            'form_url': mark_safe(''),
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(model_admin.model).id,
            'save_as': model_admin.save_as,
            'save_on_top': model_admin.save_on_top,
        },
    )


class BikeListView(ListView):
    """
         Show a list of all containers.

         **Context**
           ``containers``
               A list of instances of :model:`velafrica_sud.Container`



       """

    model = Bike
    template_name = "bikes/bike_list.html"


class BikeCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return BikeCategory.objects.all()
