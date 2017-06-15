from rest_framework import routers
from django.conf.urls import url, include

from .views import view_form, FormListView, FormCreate, \
                   UserViewSet, FormViewSet, QuestionViewSet


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    # url(r'^home/', home),
    url(r'^home/', FormListView.as_view(), name="form-list"),
    url(r'^create/', FormCreate.as_view(), name="form-create"),
    url(r'^view_form/(?P<username>\w+)/(?P<pk>\d+)$', view_form, name="view-form")
    # url(r'^api/', include(router.urls)),
]