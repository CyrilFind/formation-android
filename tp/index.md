# TP

{% for file in site.static_files %}
{% if file.path contains 'tp/' and file.name contains '.md' %}

* [{{ file.basename }}]({{ site.baseurl }}/tp/{{ file.basename }})

{% endif %}
{% endfor %}

[→ Slides](slides/)
