from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(subject, to, template, context=None):

    if isinstance(to, str):
        to = [to]

    default_context = {
        'site_url': 'https://wakfustrat.fr'
    }

    if context is not None:
        default_context = {**context, **default_context}

    body = render_to_string(template, default_context)

    msg = EmailMessage('[WakfuStrat] {0}'.format(subject), body, 'contact@wakfustrat.fr', to)
    msg.content_subtype = 'html'
    msg.send()
