from django.shortcuts import render, redirect
from django.http import *
from user.functions import *
from django.views import *
from user.models import User
from user.models import Transaction
from django.contrib import messages
from django.shortcuts import *
import datetime
import math


def showMain(request):
    if 'redirect' in request.GET:

        if request.GET['redirect'] == 'Авторизация':
            return redirect('/autorise')
        elif request.GET['redirect'] == 'Регистрация':
            return redirect('/registration')
        elif request.GET['redirect'] == 'О сайте':
            return redirect('/about')

    return render(request, 'user/main.html')


def autorise(request):
    if 'login' in request.POST:
        login = request.POST['login']
        password = request.POST['pass']
        user = User.objects.filter(login=login, password=password)
        if len(user) == 1:

            request.session['login'] = login
            request.session['pass'] = password

            return redirect('account/')
        else:
            messages.info(request, 'Такого пользователя не существует')
    return render(request, 'user/autorise.html')


def registration(request):
    if request.POST:

        if 'login' in request.POST:
            login = request.POST['login']
            password = request.POST['pass']
            rep_pass = request.POST['pass_r']

            if login != '' and password != '' and rep_pass != '':
                is_exist = User.objects.filter(login=login).exists()
                if is_exist == False:
                    if password == rep_pass:
                        user = User(login=login, password=password)
                        user.save()

                        request.session['login'] = login
                        messages.info(request, 'Вы успешно зарегистрировались, теперь авторизируйтесь')
                        return redirect('/autorise/')
                    else:
                        messages.info(request, 'Введённые пароли не совпадают!')
                        return HttpResponseRedirect('/registration')
                else:
                    messages.info(request, 'Пользователь с таким логином, уже существует!')
                    return HttpResponseRedirect('/registration')
        elif 'fonts' in request.POST:
            if 'login' in request.session:
                user_login = request.session['login']
                del request.session['login']
                request.session.modified = True
                last_user = User.objects.get(login=user_login)
                if last_user.fp == 'null':
                    hash = get_hash_peaces(get_data_for_fingerprint(request), get_fp_js(request))
                    data_base_fp_string = ''

                    for key in hash:
                        data_base_fp_string += f'{key}-{hash[key][0]},{hash[key][1]};'

                    last_user.fp = data_base_fp_string
                    last_user.save()

    return render(request, 'user/registration.html')


def about(request):
    return render(request, 'user/about.html')


def show_results(request):
    res = 'Обновите страницу'
    if 'res' in request.session:
        res = request.session['res']
    if request.POST:
        user = User.objects.get(login=request.session['login'], password=request.session['pass'])
        dabase_hash_items = user.fp.split(';')

        if user.fp != 'null':
            hash = get_hash_peaces(get_data_for_fingerprint(request), get_fp_js(request))
            hash_string = ''

            for key in hash:
                hash_string += f'{key}-{hash[key][0]},{hash[key][1]};'
            hash_items = hash_string.split(';')

            # print(hash_items)
            res = comapre_hash(dabase_hash_items, hash_items, user)

            request.session['res'] = res
            # messages.success(request, "Your data has been saved!")

    return render(request, 'user/result.html', context={'res': res})


def login(request):
    if 'redirect' in request.POST:
        if request.POST['redirect'] == 'Перевод':
            return redirect('transactions/')
        elif request.POST['redirect'] == 'Пополнить счёт':
            return redirect('addmoney/')

    user_login = request.session['login']
    user_pass = request.session['pass']

    print(user_login, user_pass)
    user = User.objects.get(login=user_login)
    request.session['active_user'] = user.id
    return render(request, 'user/account.html',
                  context={'pass': request.session['pass'], 'login': request.session['login'],
                           'money': round(user.money, 3), 'id': round(user.id)})


def go_to_transactions(request):
    try:
        get_fp_js(request)
    except:
        pass
    if 'user_to_send' in request.POST and 'money_for_transaction' in request.POST:

        user_to_send_id = 0
        user_from_sent_id = 0

        try:
            user_to_send_id = int(request.POST['user_to_send'])
            user_from_sent_id = int(request.session['active_user'])
        except:
            pass
        money_to_sent = 0

        try:

            money_to_sent = float(request.POST['money_for_transaction'])
            if money_to_sent == 0:
                raise ValueError
        except ValueError:
            messages.info(request, 'Введите сумму корректно')
            return redirect('/autorise/account/transactions/')

        try:
            user_to = User.objects.get(id=user_to_send_id)
            user_from = User.objects.get(id=user_from_sent_id)

            user_from.money -= money_to_sent
            user_to.money += money_to_sent

            transaction = makeTrancation(request, money=money_to_sent, user_from=user_from.id, user_to=user_to.id)
            value = isFraude(transaction)

            user_from.save()
            user_to.save()

            if value == 0:
                messages.info(request, 'Операция проведена успешно, фрода не обнаружено')
            else:
                messages.info(request, 'ТЫ МОШЕНИК !!!!!!!!!!!!!!!!')

            return redirect('/autorise/account/')

        except Exception as ex:
            print(ex)
            messages.info(request, 'Такого пользователя не существует')
            return redirect('/autorise/account/transactions/')

    return render(request, 'user/trasactions.html')


def add_money(request):
    if 'redirect' in request.POST:
        if request.POST['redirect'] == 'Пополнить':
            try:
                user_login = request.session['login']
                user_pass = request.session['pass']

                money = float(request.POST['money'])
                user = User.objects.get(login=user_login, password=user_pass)
                user.money += money
                user.save()
                return redirect('/autorise/account/', permanent=True)
            except ValueError:
                return render(request, 'user/addmoney.html')

    return render(request, 'user/addmoney.html')
