"""Marketplace views removed.

These are placeholders left behind after removing the marketplace feature.
They intentionally return a simple response so any accidental imports don't
cause runtime errors during cleanup. Replace or delete as needed.
"""

from django.http import HttpResponse


def removed(request):
    return HttpResponse('Marketplace has been removed.', status=410)


# Keep some named callables in case templates or code still reference them.
def home(request):
    return removed(request)


def products(request):
    return removed(request)


def inputs(request):
    return removed(request)


def orders(request):
    return removed(request)


def dashboard(request):
    return removed(request)
