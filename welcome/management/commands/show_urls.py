from __future__ import print_function
from django.core.management import BaseCommand
import urls

def show_urls(urllist, depth=0):
    """
    Prints url patterns hierarchically
    @param urllist: url list to print
    @param depth: depth of given list
    """
    for entry in urllist:
        print(" " * depth, entry.regex.pattern)
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

class Command(BaseCommand):
    help = 'Shows urlpatterns'

    def handle(self, *args, **options):
        show_urls(urls.urlpatterns)
