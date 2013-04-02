import functools
from django.views.generic import date_based
from django.core.urlresolvers import reverse

from .models import Entry

def logbook(request): 
    """Logbook homepage"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(is_active=True).order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=20, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/logbook.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )

def linked(request): 
    """Linked list (kind == Link)"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(is_active=True, kind='L').order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=30, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/linked.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )


def logbook_archive(request): 
    """Archive of original entries (kind == Article)"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(kind='A').order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=9999, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/archive.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )

# =Search

# from django.http import HttpResponse 
# from django.template import loader, Context
# 
# def search(request): 
#     query = request.GET['q']
#     results = Note.objects.filter(content_html__icontains=query)
#     template = loader.get_template('hth/search.html')
#     context = Context({ 'query': query, 'results': results })
#     response = template.render(context)
#     return HttpResponse(response)

# or use django's render_to_response shortcut:

from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext # http://stackoverflow.com/a/5478944/412329

# def search(request):
#     query = request.GET['q']
#     return render_to_response('hth/search.html',
#         {   'query': query, 
#             'results': Note.objects.filter(content_html__icontains=query) })

# rewritten so /search/ URL can be accessed directly:

def search(request):    
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    results = []
    # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    user = request.user
    if query:
        # INSTEAD OF THIS:
        # title_results = Note.objects.filter(title__icontains=query)
        # results = Note.objects.filter(content_html__icontains=query)
        # DO THIS avoid duplicate results when query word is both in title and content_html:
        # http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
        results = Entry.objects.filter(Q(title__icontains=query)|Q(body_html__icontains=query)).distinct()
    return render_to_response('hth/search.html',
        {   'query': query, 
            'results': results,
            'user': user
             }, context_instance=RequestContext(request)) # http://stackoverflow.com/a/5478944/412329