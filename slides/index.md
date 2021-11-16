# Cours

{% for file in site.static_files %}
{% if file.name contains 'slides/' or file.name contains '.html' %}

* [{{ file.basename }}]({{ site.baseurl }}{{ file.path }})

{% endif %}
{% endfor %}
