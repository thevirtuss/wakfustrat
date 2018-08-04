from django.views.generic import ListView

from wakfustrat.news.models import News


class NewsListView(ListView):
    """
    Single view of a news.
    """
    queryset = News.objects.exclude(publish_date=None).order_by('-publish_date').all()
    template_name = 'news/list.html'
