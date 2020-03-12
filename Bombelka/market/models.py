from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=100, verbose_name='')
    description = models.TextField(verbose_name='')

    photo_1 = models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='')
    photo_2 = models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='')
    photo_3 = models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='')

    SEX_TAG_CHOISE= [('Boy','Chłopca'),('Girl', 'Dziewczynki'), ('Unisex', 'Zarówno dla chłopca jaki i dziewczynki')]

    tag_sex = models.CharField(max_length=6, choices = SEX_TAG_CHOISE, default='Unisex', verbose_name='')

    tag_age = models.IntegerField(choices = [(1,'< 1 miesiąc'),
                                            (2,'< 3 miesiące'),
                                            (3,'< 6 miesięcy'),
                                            (4,'< 1 rok'),
                                            (5,'< 1.5 roku'),
                                            (6,'< 2 lata'),
                                            (7,'Ponad 2 lata')],
                                                                 default=1, verbose_name='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #         super().save(*args, **kwargs)

    #         img = Image.open(self.photo_1.path)

    #         if img.height > 300 or img.width > 300:
    #             output_size = (300,300)
    #             img.thumbnail(output_size)
    #             img.save(self.photo_1.path)


