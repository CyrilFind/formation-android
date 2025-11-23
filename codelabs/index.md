# Codelabs

[→ Slides](slides/)

{% for file in site.static_files %}
{% if file.path contains 'codelabs/' and file.name contains '.html' %}
{% assign pathSegments = file.path | split: "/"  %}

* [{{ pathSegments[-2]}}]({{ site.baseurl }}{{ file.path }})

{% endif %}
{% endfor %}

[→ Markdown](../tp/)

[→ Slides](slides/)
