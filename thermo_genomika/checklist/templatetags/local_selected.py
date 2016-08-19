from django import template

register = template.Library()


@register.assignment_tag
def get_selected(local_pk, room_pk):
    if local_pk == str(room_pk):
        return 'selected'
