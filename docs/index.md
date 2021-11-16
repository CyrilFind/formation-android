# Cours

{% for file in site.static_files %}
    {% if file.name contains '.md' or file.name contains '.html' %}
*[{{ file.name }}]({{ site.baseurl }}{{ file.path }})
    {% endif %}
{% endfor %}
