from django.contrib.auth.decorators import login_required
from django.db import models
from dish_app.models import Dish, Product


class Document(models.Model):
    CHOICES_TYPE = (('0', 'Поступление'), ('1', 'Списание'))
    name = models.CharField(max_length=256, blank=False, null=False, verbose_name='Наименование документа')
    number = models.CharField(max_length=256, blank=False, null=False, verbose_name='Номер документа')
    document_type = models.CharField(max_length=128, blank=False, null=False, verbose_name='Тип документа',
                                     choices=CHOICES_TYPE)
    date = models.DateField(verbose_name='Дата документа')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарии')
    document_status = models.BooleanField(verbose_name='Проводка документа')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return '%s %s %s' % (self.name, self.number, self.date)


class MovingProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.DecimalField(max_digits=16, decimal_places=3, verbose_name='Количество')
    date = models.DateField(verbose_name='Дата операции')
    document = models.ForeignKey(Document, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                    verbose_name='Входящий документ')
    operation_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Движение товаров'
        verbose_name_plural = 'Движение товаров'

    def __str__(self):
        return str(self.date) + ' ' + str(self.product) + ' ' + str(self.count)

    def save(self, *args, **kwargs):
        super(MovingProducts, self).save(*args, **kwargs)
        self.operation_status = self.document.document_status



class ProductsInDocument(models.Model):
    document = models.ForeignKey(Document, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Документ')
    data = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт в документе'
        verbose_name_plural = "Продукты в документах"
        ordering = ['data']

    def __str__(self):
        return '%s %s%s' % (str(self.data), str(self.count), self.data.unit)


class DishInDocument(models.Model):
    document = models.ForeignKey(Document, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Документ')
    data = models.ForeignKey(Dish, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Количество')

    class Meta:
        verbose_name = 'Блюдо в документе'
        verbose_name_plural = "Блюда в документах"
        ordering = ['data']

    def __str__(self):
        return '%s %s'%(str(self.data), str(self.count))