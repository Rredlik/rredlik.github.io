from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from users.forms import UserForm, TaskForm
from users.models import Task, Core, Boost
from users.serializer import CoreSerializer, BoostSerializer
from .constants import CASUAL_BOOSTS_VALUES


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            core = Core(user=user)
            core.save()
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def UserLoginView(request):
    form = UserForm()

    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Аккаунт отлючен!')
        else:
            return HttpResponse('Не верный логин')
        return render(request, 'login.html', {'form': form, 'invalid': True})

    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def taskTables(request):
    tasks = Task.objects.all()
    return render(request, 'users/taskTables.html', {'title': 'Cтраница с задачами', 'tasks': tasks})


def taskCreate(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables')
        else:
            error = 'Форма была неверной'

    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'users/taskCreate.html', context)


class CookieView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            cookie = Task.objects.filter(pk=id)
            return Response(cookie.values())

        cookies = Task.objects.all()
        return Response(cookies.values())

    def post(self, request):
        title = request.data.get('title')
        task = request.data.get('task')

        if title and task:
            cookie = Task.objects.create(title=title, task=task)
            return Response({
                'id': cookie.id,
                'title': cookie.title,
                'task': cookie.task,
            })
        return Response({'Error': 'Invalid data'})

    def put(self, request):
        id = request.data.get('id')
        if id:
            cookie = Task.objects.filter(pk=id)
            cookie.update(
                title=request.data.get('title'),
                task=request.data.get('task'),
            )
            return Response(cookie.values())
        return Response({'Error': 'Invalid data'})

    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            cookie = Task.objects.get(pk=id)
            cookie.delete()
            return Response({'Response': f'task {id} deleted'})
        return Response({'Error': 'Invalid data'})


@login_required
def Game(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)
    game_context = {
        'core': core,
        'boosts': boosts,
    }

    return render(request, 'users/game.html', game_context)


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({
        'core': CoreSerializer(core).data,
    })


@api_view(['POST'])
def update_coins(request):
    coins = request.data['current_coins']
    core = Core.objects.get(user=request.user)
    is_levelup, boost_type = core.update_coins(coins)

    if is_levelup and core.level <= 10:
        Boost.objects.create(
            core=core,
            price=CASUAL_BOOSTS_VALUES[core.level - 1]['base_price'],
            power=CASUAL_BOOSTS_VALUES[core.level - 1]['base_click_power'],
            type=boost_type,
        )
    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)

        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']
        boost = self.queryset.get(pk=pk)
        levelup = boost.levelup(coins)
        if not levelup:
            return Response({'error': 'Недостоточно монеток'})
        old_boost_values, new_boost_values = levelup
        return Response({
            'old_boost_values': self.serializer_class(old_boost_values).data,
            'new_boost_values': self.serializer_class(new_boost_values).data,
        })
