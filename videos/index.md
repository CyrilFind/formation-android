# Videos

{% for video in site.videos %}

## {{video.title}}

<iframe class="media" src="{{video.url}}" title="{{video.title}}" width="100%" height="350" style="max-width: 600px;outline: none" allow="encrypted-media; picture-in-picture" frameborder="0" allowfullscreen=""></iframe>

{% endfor %}
