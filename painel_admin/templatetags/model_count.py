from django import template
from django.apps import apps

register = template.Library()

@register.simple_tag
def model_total(app_label, model_name):
    model = apps.get_model(app_label, model_name)
    return model.objects.count()