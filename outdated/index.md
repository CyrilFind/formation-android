# Archive

{% for file in site.static_files %}
{% if file.path contains 'outdated/' and file.name contains '.md' %}

* [{{ file.basename }}]({{ site.baseurl }}/outdated/{{ file.basename }})

{% endif %}
{% endfor %}
