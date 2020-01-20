from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlquote
from weasyprint import HTML


def encode_filename(filename):
    """
    Encodes filename part for ``Content-Disposition: attachment``.

    filename="abc.pdf" => filename=abc.pdf
    filename="aa bb.pdf" => filename*=UTF-8''aa%20bb.pdf
    filename=u"zażółć.pdf" => filename*=UTF-8''za%C5%BC%C3%B3%C5%82%C4%87.pdf
    """

    quoted = urlquote(filename)
    if quoted == filename:
        return "filename=%s" % filename
    else:
        return "filename*=UTF-8''%s" % quoted


def make_response(content, filename=None, content_type="application/pdf"):
    """
    Wraps content into HTTP response.

    If ``filename`` is specified then ``Content-Disposition: attachment``
    header is added to the response.

    Default ``Content-Type`` is ``application/pdf``.

    :param bytes content: response content
    :param str filename: optional filename for file download
    :param str content_type: response content type
    :rtype: :class:`django.http.HttpResponse`
    """
    response = HttpResponse(content, content_type=content_type)
    if filename is not None:
        response["Content-Disposition"] = "attachment; {}".format(
            encode_filename(filename)
        )
    return response


def render_to_pdf(request, template, context, base_url=None, filename=None, stylesheets=None):
    return make_response(
        content=HTML(
            string=render_to_string(
                request=request,
                template_name=template,
                context=context
            ),
            base_url=base_url or request.build_absolute_uri()
        ).write_pdf(stylesheets=stylesheets),
        filename=filename
    )