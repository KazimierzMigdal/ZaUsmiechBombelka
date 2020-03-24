from django.shortcuts import render
from .models import Action
from django.contrib.auth.models import User
from market.models import Product
from users.models import Profile
from django.db.models import Q

def actions(request):
    actions=Action.objects.all()
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')

    products = Product.objects.all()[:4]
    interested_sex_tag = request.user.profile.interested_sex_tag
    interested_age_tag = request.user.profile.interested_age_tag

    #best match for profile recomendation
    best_profile_match = User.objects.all().filter(
            Q(profile__sold_sex_tag = interested_age_tag) & Q(profile__sold_sex_tag = interested_sex_tag)
                ).exclude(id=request.user.id).order_by('-total_followers')
    #secound match for profile recomendation
    if interested_sex_tag != 'Unisex':
        secound_profile_match = User.objects.all().filter(
            Q(profile__sold_age_tag = interested_age_tag) & Q(profile__sold_sex_tag = 'Unisex')
                ).exclude(id=request.user.id).order_by('-total_followers')
    else:
        secound_profile_match = User.objects.all().filter(
            Q(profile__sold_age_tag = interested_age_tag) & (Q(profile__sold_sex_tag = 'Boy') | Q(profile__sold_sex_tag = 'Girl'))
                ).exclude(id=request.user.id).order_by('-total_followers')
    #third match for profile recomendation
    if interested_age_tag != 7 or interested_age_tag != 1:
        third_profile_match = User.objects.all().filter(
            (Q(profile__sold_age_tag = interested_age_tag-1) | Q(profile__sold_age_tag = interested_age_tag+1)) & Q(profile__sold_sex_tag = interested_sex_tag)
            ).exclude(id=request.user.id).order_by('-total_followers')
    elif interested_age_tag != 7:
        third_match = User.objects.all().filter(
            (Q(profile__sold_age_tag = interested_age_tag-1) | Q(profile__sold_age_tag = interested_age_tag-2)) & Q(profile__sold_sex_tag = interested_sex_tag)
            ).exclude(id=request.user.id).order_by('-total_followers')
    else:
        third_profile_match = User.objects.all().filter(
            (Q(profile__sold_age_tag = interested_age_tag+1) | Q(profile__sold_age_tag = interested_age_tag+2)) & Q(profile__sold_sex_tag = interested_sex_tag)
            ).exclude(id=request.user.id).order_by('-total_followers')

    users = best_profile_match | secound_profile_match | third_profile_match

    #fourth match for profile recomendation
    if len(users) < 4:
        users|= User.objects.all().exclude(id=request.user.id).order_by('-total_followers')
    users = users[:4]

    #best match for product recomendation
    best_product_match = Product.objects.all().filter(
        Q(tag_sex=interested_sex_tag)&Q(tag_age=interested_age_tag)
        ).exclude(author=request.user)
    #secound match for product recomendation
    if interested_sex_tag != 'Unisex':
        secoud_product_match = Product.objects.all().filter(
        Q(tag_sex='Unisex')&Q(tag_age=interested_age_tag)
          ).exclude(author=request.user)
    else:
        secoud_product_match = Product.objects.all().filter(
        (Q(tag_sex='Boy')|Q(tag_sex='Girl'))&Q(tag_age=interested_age_tag)
          ).exclude(author=request.user)
    #third match for profile recomendation
    if interested_age_tag != 7 or interested_age_tag != 1:
        third_product_match = Product.objects.all().filter(
            (Q(tag_age = interested_age_tag-1) | Q(tag_age = interested_age_tag+1)) & Q(tag_sex = interested_sex_tag)
            ).exclude(author=request.user)
    elif interested_age_tag == 7:
        third_product_match = Product.objects.all().filter(
        (Q(tag_age = interested_age_tag-1) | Q(tag_age = interested_age_tag-2)) & Q(tag_sex = interested_sex_tag)
        ).exclude(author=request.user)
    else:
        third_product_match = Product.objects.all().filter(
            (Q(tag_age = interested_age_tag+1) | Q(tag_age = interested_age_tag+2)) & Q(tag_sex = interested_sex_tag)
            ).exclude(author=request.user)

    products = best_product_match | secoud_product_match | third_product_match
    #fourth match for profile recomendation
    if len(products)<4:
        products|= Product.objects.all().exclude(author=request.user)

    products = products[:4]

    return render(request, 'actions/action/detail.html', {'section': 'actions',
                                                        'actions': actions,
                                                        'products': products,
                                                        'users':users})
