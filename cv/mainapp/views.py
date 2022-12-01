from pyexpat.errors import messages

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView

from mainapp.forms import NameForm, EmailForm, SubjectForm, MessageForm, CreateCommentForm
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

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()
        )
        comment_form = CreateCommentForm()
        context['comment_form'] = comment_form

        return context


class CommentCreateView(CreateView):
    template_name = 'mainapp/comment.html'
    model = Comment
    form_class = CreateCommentForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def send_verify_link(self, comment):
        verify_link = reverse('verify', args=[comment.email, comment.activation_key])
        subject = f'Для комментирования на сайте http://polinanechaeva.pythonanywhere.com пройдите по ссылке'
        message = f'Для того, чтобы оставить комментарий под именем {comment.user_name} на портале\n' \
                  f'{settings.DOMAIN_NAME} необходимо подтвердить адрес e-mail, для этого пройдите по ссылке' \
                  f' {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [comment.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        comment_form = self.form_class(self.request.POST, self.request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save()
            self.send_verify_link(comment)
            return HttpResponseRedirect(reverse('comment'))
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return super().get(request, *args, **kwargs)
            # return HttpResponse('Неверно заполненная форма. Попробуйте еще раз.')


def verify(request, email, activation_key):
    try:
        comment = Comment.objects.get(email=email)
        if comment.activation_key == activation_key and not comment.is_activation_key_expired():
            comment.is_checked = True
            comment.save()
            return render(request, 'mainapp/varification.html')
        else:
            print(f'error activation user: {comment}')
            return render(request, 'mainapp/varification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


class EmailListView(View):
    form_class1 = NameForm
    form_class2 = EmailForm
    form_class3 = SubjectForm
    form_class4 = MessageForm

    def get(self, request):
        return redirect("contact")

    def post(self, request):

        name_form = self.form_class1(request.POST)
        email_form = self.form_class2(request.POST)
        subject_form = self.form_class3(request.POST)
        message_form = self.form_class4(request.POST)

        if name_form.is_valid() and email_form.is_valid() and subject_form.is_valid() and message_form.is_valid():
            body = {
                'name': name_form.cleaned_data['name'],
                'subject': subject_form.cleaned_data['subject'],
                'email': email_form.cleaned_data['email_address'],
                'message': message_form.cleaned_data['message'],
            }
            subject = f"Клиентский запрос, ТЕМА: {body['subject']}"
            message = f'Email: {body["email"]}\nName:{body["name"]}\nMessage:\n{body["message"]}.'
            print((subject, message, settings.EMAIL_HOST_USER, ['polina2000_21@mail.ru']))
            try:
                print(f'sending message: {message}')
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['polina2000_21@mail.ru'])
            except BadHeaderError:
                print('Nope')
                return HttpResponse('Invalid header found.')
            return redirect("contact")
        else:
            return HttpResponse('Данные введены неверно, попробуйте еще раз.', charset="utf-8")
