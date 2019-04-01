from threading import Thread

from flask import url_for, current_app, render_template
from flask_mail import Message

from originblog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, template, **kwargs):
    app = current_app._get_current_object()  # 获取被代理的真实对象
    message = Message(subject=current_app.config['APP_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.body = render_template(template + '.html', **kwargs)
    thr = Thread(target=_send_async_mail, args=(app, message))
    thr.start()
    return thr


def send_confirm_email(user, token, to=None):
    send_mail(subject='Email Confirm', to=to or user.email, template='emails/confirm', user=user, token=token)


def send_reset_password_email(user, token):
    send_mail(subject='Password Reset', to=user.email, template='emails/reset_password', user=user, token=token)


def send_change_email_email(user, token, to=None):
    send_mail(subject='Change Email', to=to or user.email, template='emails/change_email', user=user, token=token)


def send_new_comment_email(post):
    send_mail(subject='New Comment', to=post.author.email, template='emails/new_comment', post=post)


def send_new_reply_email(comment):
    send_mail(subject='New Reply', to=comment.email, template='emails/new_reply', comment=comment)