from pathlib import Path

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ratelimit.decorators import ratelimit

from utility import TextSimilarity, read_single_col_in_dataset

file_path = Path(__file__).parent.parent.resolve()
DUMMY_MEDICAL_CSV = f'{file_path}/utility/Dummy medical dataset.csv'


@require_http_methods(["GET"])
@ratelimit(key='ip', rate='5/m', block=True)
def index(request):
    """This function is called when the user open the site
     Args:
         (object) request - contain request objects
     Return:
         http response contains the list of keys that used for similarity searching
    """
    medical_keys = read_single_col_in_dataset('Key', DUMMY_MEDICAL_CSV)
    return render(request, 'text_matching/index.html', {"keys": medical_keys})


@require_http_methods(["POST"])
@ratelimit(key='ip', rate='5/m', block=True)
def search(request):
    """This function is called when the user searches for similarity
    between the key he sends and the dummy medical values column in CSV
     Args:
         (object) request - contains request objects and the key that user sends it
     Return:
         http response contains two keys one for the key sent and other list of matching texts with that key
    """
    search_key = request.POST.get("key", None)
    if not search_key:
        messages.error(request, "Error search key not sent.")
    text_similarity = TextSimilarity(search_key, percentage=50)
    medical_values = read_single_col_in_dataset('Values', DUMMY_MEDICAL_CSV)
    matching_text = text_similarity.search_for_similarity(medical_values)
    if matching_text:
        return render(request, 'text_matching/similarity_table.html',
                      {"matching_text": matching_text, "key": search_key})
    else:
        messages.warning(request, "There is no similarity found.")
    return redirect('text_matching:index')


def handler429(request, exception):
    """This function are called when too many request occurs on endpoint
    when user exceed the maximum number of requests
    """
    template_name = 'text_matching/error_429.html'
    return render(request, template_name, locals())
