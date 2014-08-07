# filters.py
from django.shortcuts import render
from django.template import Template, Context

def inject_map(tpl):
    template = Template(tpl)
    content = template.render(Context({'geom': '<div id="map"></div>'}))
    return content