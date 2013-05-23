from django.views import generic
from tournaments.models import Tournament

class IndexView(generic.ListView):
    template_name = 'tournaments/index.html'
    context_object_name = 'tournaments_list'

    def get_queryset(self):
        return Tournament.objects.order_by('-start_date')
    
    
class DetailView(generic.DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'    