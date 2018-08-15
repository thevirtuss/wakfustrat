from django.urls import path

from wakfustrat.wiki.views import PageCreateView, PageUpdateView, WikiHistoryView, ImageUploadView, PageDetailView, \
    PageListView, WikiImagesView

app_name = 'wiki'
urlpatterns = [
    path('image/upload/', ImageUploadView.as_view(), name='upload-image'),
    path('<str:part>/management/nouveau/', PageCreateView.as_view(), name='page-create'),
    path('<str:part>/<str:slug>/édition/', PageUpdateView.as_view(), name='page-update'),
    path('<str:part>/<str:slug>/historique/', WikiHistoryView.as_view(), name='history'),
    path('<str:part>/<str:slug>/images/', WikiImagesView.as_view(), name='images'),
    path('<str:part>/<str:slug>/', PageDetailView.as_view(), name='page-detail'),
    path('<str:part>/', PageListView.as_view(), name='page-list'),

]
