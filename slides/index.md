# Cours

[→ TPs](../codelabs/)

{% for file in site.static_files %}
{% if file.path contains 'slides/' and file.name contains '.html' %}

* [{{ file.basename }}]({{ site.baseurl }}{{ file.path }})

{% endif %}
{% endfor %}

[→ TPs](../codelabs/)
