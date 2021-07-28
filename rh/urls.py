from django.conf.urls import url
from .views import TagAutocomplete

urlpatterns = [
    url(
        r'^tags-autocomplete/$',
        TagAutocomplete.as_view(),
        name='tags-autocomplete',
    ),
]