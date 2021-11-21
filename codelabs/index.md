# Codelabs

⚠️ Selon les classes et le temps disponible nous ne feront pas forcément tout ça:

{% for file in site.static_files %}
{% if file.path contains 'codelabs/' and file.name contains '.html' %}
{% assign pathSegments = file.path | split: "/"  %}

* [{{ pathSegments[-2]}}]({{ site.baseurl }}{{ file.path }})

{% endif %}
{% endfor %}
