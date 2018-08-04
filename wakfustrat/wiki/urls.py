from django.urls import path

from wakfustrat.wiki.views import NewDungeonView, DungeonListView, DungeonDetailView, DungeonUpdateView, \
    WikiHistoryView, ImageUploadView


urlpatterns = [
    path('image/upload/', ImageUploadView.as_view(), name='upload-image'),
    path('<str:part>/<str:slug>/history/', WikiHistoryView.as_view(), name='wiki-history'),

    path('donjons/management/nouveau/', NewDungeonView.as_view(), name='new-dungeon'),
    path('donjons/management/edit/<str:slug>/', DungeonUpdateView.as_view(), name='dungeon-update'),
    path('donjons/<str:slug>/', DungeonDetailView.as_view(), name='dungeon-detail'),
    path('donjons/', DungeonListView.as_view(), name='dungeon-list'),

]
