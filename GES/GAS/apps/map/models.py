from django.db import models


class MAP(models.Model):
    id = models.Index('id', name='Id страницы')
    idOfPage = id
    page_id = id
<<<<<<< HEAD
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('published', 'Опубликовано'),
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES)
    nameOfPage = models.CharField('Имя страницы', max_length= 50)
=======
    FlagForInternalRecordings = models.IntegerField('Флаг на наличие подкатегорий')
    nameOfPage = models.CharField('Имя категории', max_length=50)
    FlagForThePresenceOfAParent = models.IntegerField('Флаг наличия родительской категории')
    internal_pages = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_pages')
    countOfVW = models.IntegerField('Количество миров', default=0)
    parent_page = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_pages')


>>>>>>> master
    def __str__(self):
        return self.nameOfPage

    class Meta:
<<<<<<< HEAD
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
=======
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def get_parent_categories(self):
            # Получаем родительские категории, в которые входит данная категория
            parent_categories = MAP.objects.filter(internal_pages=self)
            return parent_categories




def countOfVirW(VWS):
    
    Pages = MAP.objects.all()
    for Page in Pages:
        Page.countOfVW = 0
        Page.save()

    startPages = MAP.objects.filter(FlagForInternalRecordings=0)     
    for startPage in startPages:
        for VW in VWS:
             if VW.map == startPage:
                startPage.countOfVW += 1
        startPage.save()
        #print('Количество внутренних миров категории ', startPage.nameOfPage , 'равно ', startPage.countOfVW)
    
        page = startPage
        while page.FlagForThePresenceOfAParent == 1:
            parentPages = page.get_parent_categories()

            for parentPage in parentPages:
                parentPage.countOfVW += startPage.countOfVW
                #print('Количество внутренних миров категории ', parentPage.nameOfPage , 'равно ', parentPage.countOfVW)
                parentPage.save()

            page = parentPages.first()  # Выберите одну родительскую страницу для следующей итерации
>>>>>>> master
