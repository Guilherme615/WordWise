# context_processors.py

def sidebar_template(request):
    return {'sidebar_template': getattr(request, 'sidebar_template', 'includes/sidebar03.html')}
