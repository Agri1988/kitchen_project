from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name='Наименование категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return '%s' % self.name


class Dish (models.Model):
    name = models.CharField(max_length=512, blank=False, null=False, verbose_name='Наименование блюда')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Категория')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = "Блюда"
        ordering = ['name']

    def __str__(self):
        return '%s %s' % (self.category.name, self.name)


class Ingredients(models.Model):
    dish = models.ForeignKey('Dish', blank=False, null=False, on_delete=models.CASCADE,
                                verbose_name='Блюдо')
    product = models.ForeignKey('Product', blank=False, null=False, on_delete=models.CASCADE,
                                verbose_name='Продукт')
    quantity = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='Количество продукта')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = "Ингредиент"
        ordering = ['dish']

    def __str__(self):
        return '%s %s%s' % (self.product.name, self.quantity, self.product.unit)


class Product(models.Model):
    CHOICE_UNIT = (('1', 'кг.'), ('2', 'гр.'), ('3', 'л.'), ('4', 'мл.'))
    name = models.CharField(max_length=512, blank=False, null=False, verbose_name='Наименование продукта')
    unit = models.CharField(max_length=16, blank=False, null=False, verbose_name='Единица измерения',
                            choices=CHOICE_UNIT)
    category = models.ForeignKey('ProductCategory', blank=False, null=False, on_delete=models.CASCADE,
                                 verbose_name='Наименование категории')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Product, self).save(*args, **kwargs)



class ProductCategory(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False, verbose_name='Наименование категории')

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = "Категории продуктов"
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)



