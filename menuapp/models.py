from django.db import models


class MenuItem(models.Model):
    """Модель, которая представляет каждый пункт меню в древовидной структуре меню"""
    title = models.CharField(
        max_length=50,
        help_text="Это название пункта меню",
    )
    url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="URL-адрес, на который будет перенаправлен пользователь при нажатии на пункт меню.\n"
                  "Он может быть пустым, если вместо URL используется именованный URL.",
    )
    named_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Именованный URL, на который будет перенаправлен пользователь при нажатии на пункт меню. \n"
                  "Он может быть пустым, если вместо него используется обычный URL.",
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Поле указывает на родительский пункт меню. Если значение этого поля пустое, то это означает, \n"
                  "что этот пункт меню является корневым элементом.",
    )
    menu_name = models.CharField(
        max_length=50,
        help_text="это имя меню, к которому относится данный пункт. \n"
                  "Это позволяет иметь несколько меню на сайте и использовать их на разных страницах.",
    )

    def __str__(self):
        return self.title
