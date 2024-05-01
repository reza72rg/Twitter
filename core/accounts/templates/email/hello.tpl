{% extends "mail_templated/base.tpl" %}

{% block subject %}
Email
{% endblock %}

{% block body %}
{{token}}
{% endblock %}

{% block html %}

{% endblock %}
