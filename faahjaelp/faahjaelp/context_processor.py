# GET THE EXAMPLE FROM http://www.b-list.org/weblog/2006/jun/14/django-tips-template-context-processors/
from job.models import JobGenre
def allJobGenre(request):
    all_job_genres=JobGenre.objects.all()
    return {'all_job_genres': all_job_genres}
