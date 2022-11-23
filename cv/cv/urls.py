from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from cv import settings
from mainapp.views import MainListView, AboutListView, WorksListView, ContactListView, EducationListView, \
    CommentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/', MainListView.as_view(), name='index'),
    path('', AboutListView.as_view(), name='about'),
    path('works/', WorksListView.as_view(), name='works'),
    path('contact/', ContactListView.as_view(), name='contact'),
    path('education/', EducationListView.as_view(), name='education'),
    path('comment/', CommentListView.as_view(), name='comment'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
