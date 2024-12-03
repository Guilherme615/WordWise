# middleware.py

from django.contrib.auth.models import Group

class SidebarMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_groups = request.user.groups.all()

            if user_groups:
                # Priorize a escolha da sidebar de acordo com a ordem de prioridade dos grupos
                priority_groups = ['Administrador', 'Professor']
                for group_name in priority_groups:
                    if group_name == 'Administrador' and group_name in [group.name for group in user_groups]:
                        request.sidebar_template = f"includes/sidebar_administrador.html"
                        break
                    elif group_name == 'Professor' and group_name in [group.name for group in user_groups]:
                        request.sidebar_template = f"includes/sidebar_professor.html"
                        break
                else:
                    request.sidebar_template = "includes/sidebar03.html"
            else:
                request.sidebar_template = "includes/sidebar03.html"
        else:
            request.sidebar_template = "includes/sidebar03.html"

        response = self.get_response(request)
        return response
