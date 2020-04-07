from .models import Action
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import (Paginator,
                                EmptyPage,
                                PageNotAnInteger)
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from market.models import Product
from users.models import Profile
import redis

r=redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db = settings.REDIS_DB)


def actions(request):
    #actions selector
    following_ids = request.user.following.values_list('id',flat=True)
    actions = []
    if following_ids:
        actions = Action.objects.exclude(user=request.user).filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')

    #profile recomendation
    interested_sex_tag = request.user.profile.interested_sex_tag
    interested_age_tag = request.user.profile.interested_age_tag
    Users = User.objects.all().exclude(id=request.user.id)
    best_profile_match = Users.filter(
            Q(profile__sold_sex_tag = interested_age_tag) & Q(profile__sold_sex_tag = interested_sex_tag)
                ).order_by('-total_followers')

    if interested_sex_tag != 'Unisex':
        secound_profile_match = Users.filter(
            Q(profile__sold_age_tag = interested_age_tag) & Q(profile__sold_sex_tag = 'Unisex')
                ).order_by('-total_followers')
    else:
        secound_profile_match = Users.filter(
            Q(profile__sold_age_tag = interested_age_tag)\
            & (Q(profile__sold_sex_tag = 'Boy') | Q(profile__sold_sex_tag = 'Girl'))
                ).order_by('-total_followers')

    if interested_age_tag != 7 or interested_age_tag != 1:
        third_profile_match = Users.filter(
            (Q(profile__sold_age_tag = interested_age_tag-1) | Q(profile__sold_age_tag = interested_age_tag+1))\
            & Q(profile__sold_sex_tag = interested_sex_tag)
            ).order_by('-total_followers')
    elif interested_age_tag != 7:
        third_profile_match = Users.filter(
            (Q(profile__sold_age_tag = interested_age_tag-1) | Q(profile__sold_age_tag = interested_age_tag-2))\
            & Q(profile__sold_sex_tag = interested_sex_tag)
            ).order_by('-total_followers')
    else:
        third_profile_match = Users.filter(
            (Q(profile__sold_age_tag = interested_age_tag+1) | Q(profile__sold_age_tag = interested_age_tag+2))\
            & Q(profile__sold_sex_tag = interested_sex_tag)
            ).order_by('-total_followers')


    users = best_profile_match | secound_profile_match | third_profile_match
    if len(users) < 4:
        users|= Users.order_by('-total_followers')
    users = users[:4]

    #product recomendation
    product_ranking = r.zrange('product_ranking', 0, -1, desc=True)
    product_ranking_ids = [int(id) for id in product_ranking]
    Products = Product.objects.all().exclude(author=request.user).exclude(author=request.user)
    best_product_match = Products.filter(
        Q(tag_sex=interested_sex_tag)&Q(tag_age=interested_age_tag)
        )

    if interested_sex_tag != 'Unisex':
        secoud_product_match = Products.filter(
        Q(tag_sex='Unisex')&Q(tag_age=interested_age_tag)
          )
    else:
        secoud_product_match = list(Products.filter(
        (Q(tag_sex='Boy')|Q(tag_sex='Girl'))&Q(tag_age=interested_age_tag)
        ))

    if interested_age_tag != 7 or interested_age_tag != 1:
        third_product_match = Products.filter(
            (Q(tag_age = interested_age_tag-1) | Q(tag_age = interested_age_tag+1))\
            & Q(tag_sex = interested_sex_tag)
            )
    elif interested_age_tag == 7:
        third_product_match = list(Products.filter(
        (Q(tag_age = interested_age_tag-1) | Q(tag_age = interested_age_tag-2))\
        & Q(tag_sex = interested_sex_tag)
        ))
    else:
        third_product_match = Products.filter(
            ((Q(tag_age = interested_age_tag+1) | Q(tag_age = interested_age_tag+2))\
            & Q(tag_sex = interested_sex_tag)
            ))

    products = []
    for QuerySet in [best_product_match, secoud_product_match, third_product_match]:
        QuerySet = list(QuerySet)
        try:
            QuerySet.sort(key=lambda x: product_ranking_ids.index(x.id))
            products = products + QuerySet
        except:
             products = products + QuerySet

    if len(products)<4:
        p = list(Products)
        products = products + p

    products = products[:4]

    #pagination
    paginator = Paginator(actions, 3)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                    'actions/action/list_ajax.html',
                    {'section': 'actions',
                    'actions': actions,
                    'products': products,
                    'users':users})

    return render(request,
                'actions/action/detail.html',
                {'section': 'actions',
                'actions': actions,
                'products': products,
                'users':users})


