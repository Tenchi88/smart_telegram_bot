from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from graphene_django.views import GraphQLView

from web.schema import schema
from nodes_app import views as nodes_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^nodes/$', nodes_views.NodeListView.as_view()),
    url(
        r'^nodes/(?P<pk>[0-9]+)/$',
        nodes_views.NodeDetailView.as_view(),
        name='node_detail',
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns