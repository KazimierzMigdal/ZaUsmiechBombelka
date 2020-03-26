from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Profile(models.Model):
    SEX_TAG_CHOISE = [('Boy','dla chłopca'),('Girl', 'dla dziewczynki'), ('Unisex', 'zarówno dla chłopca jaki i dziewczynki')]
    AGE_TAG_CHOISE =[(1,'< 1 miesiąca'),(2,'< 3 miesiący'),(3,'< 6 miesięcy'),(4,'< 1 rok'),(5,'< 1.5 roku'),(6,'< 2 lat'),(7,'Ponad 2 lat')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(default='Brak opisu')
    interested_sex_tag = models.CharField(max_length=6, choices = SEX_TAG_CHOISE, default='Unisex')
    interested_age_tag = models.IntegerField(choices=AGE_TAG_CHOISE, default=1)
    sold_sex_tag = models.CharField(max_length=6, choices = SEX_TAG_CHOISE, default='Unisex')
    sold_age_tag = models.IntegerField(choices=AGE_TAG_CHOISE, default=1)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Contact(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)



User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))


User.add_to_class('total_followers',
                  models.PositiveIntegerField(db_index=True, default=0))




