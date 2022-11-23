from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.views.generic import ListView

from mainapp.forms import NameForm, EmailForm, SubjectForm, MessageForm
from mainapp.models import Comment, Certificate


class TitleContextMixin:

    def get_title(self):
        return getattr(self, 'title', '')

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()

        )
        return context


class MainListView(TitleContextMixin, ListView):
    title = 'Отзывы'
    template_name = 'mainapp/review.html'
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()
        )
        context['comment_list'] = Comment.objects.filter(is_checked=True).order_by('?')[:9]
        return context


class AboutListView(TitleContextMixin, ListView):
    title = 'Главная'
    template_name = 'mainapp/index.html'
    model = User


class WorksListView(TitleContextMixin, ListView):
    title = 'Работы'
    template_name = 'mainapp/works.html'
    model = User


class ContactListView(TitleContextMixin, ListView):
    title = 'Контакты'
    template_name = 'mainapp/contact.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()
        )
        name_form = NameForm()
        email_form = EmailForm()
        subject_form = SubjectForm()
        message_form = MessageForm()
        context['name_form'] = name_form
        context['email_form'] = email_form
        context['subject_form'] = subject_form
        context['message_form'] = message_form
        return context


class EducationListView(TitleContextMixin, ListView):
    title = 'Образование'
    template_name = 'mainapp/education.html'
    model = Certificate

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()
        )
        context['course_list'] = Certificate.objects.order_by(Lower('add_datetime').desc())
        return context


class CommentListView(TitleContextMixin, ListView):
    title = 'Оставить комментарий'
    template_name = 'mainapp/comment.html'
    model = Comment
