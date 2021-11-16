# TP

⚠️ Selon les classes et le temps disponible nous ne feront pas forcément tout ça:

{% for file in site.static_files %}
{% if file.name contains 'tp/' or file.name contains '.html' %}

* [{{ file.basename }}]({{ site.baseurl }}{{ file.path }})

{% endif %}
{% endfor %}
