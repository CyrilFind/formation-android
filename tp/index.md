# TP

⚠️ Selon les classes et le temps disponible nous ne feront pas forcément tout ça:

{% for file in site.static_files %}
{% if file.path contains 'tp/' and file.name contains '.md' %}

* [{{ file.basename }}]({{ site.baseurl }}{{ file.basename }}.html)

{% endif %}
{% endfor %}
