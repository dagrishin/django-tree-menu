from django.test import TestCase
from django.urls import reverse

from .models import MenuItem
from .templatetags.menu_tags import get_menu_items, render_menu


class MenuTests(TestCase):
    def setUp(self):
        # Создаем тестовые меню
        menu1 = MenuItem.objects.create(title='Menu 1', url='/menu1/', menu_name='menu1')
        menu2 = MenuItem.objects.create(title='Menu 2', url='/menu2/', menu_name='menu1')
        menu3 = MenuItem.objects.create(title='Menu 3', url='/menu3/', menu_name='menu2', parent=menu2)
        menu4 = MenuItem.objects.create(title='Menu 4', url='/menu4/', menu_name='menu2', parent=menu3)
        menu5 = MenuItem.objects.create(title='Menu 5', named_url='home', menu_name='menu1')

        # Создаем тестовые URL'ы
        self.url1 = '/menu1/'
        self.url2 = '/menu2/'
        self.url3 = '/menu3/'
        self.url4 = '/menu4/'
        self.url5 = reverse('home')

    def test_menu_item_creation(self):
        # Проверяем создание меню
        menu1 = MenuItem.objects.get(title='Menu 1')
        menu2 = MenuItem.objects.get(title='Menu 2')
        menu3 = MenuItem.objects.get(title='Menu 3')
        menu4 = MenuItem.objects.get(title='Menu 4')
        menu5 = MenuItem.objects.get(title='Menu 5')

        self.assertEqual(menu1.url, '/menu1/')
        self.assertEqual(menu2.menu_name, 'menu1')
        self.assertEqual(menu3.parent.title, 'Menu 2')
        self.assertEqual(menu4.named_url, None)
        self.assertEqual(menu5.url, None)

    def test_get_menu_items(self):
        # Проверяем корректность формирования списка меню
        menu_items = get_menu_items('menu1', self.url1)
        self.assertEqual(len(menu_items), 3)
        self.assertEqual(menu_items[0]['title'], 'Menu 1')
        self.assertEqual(menu_items[1]['title'], 'Menu 2')
        self.assertEqual(menu_items[2]['title'], 'Menu 5')
        self.assertTrue(menu_items[0]['is_active'])
        self.assertFalse(menu_items[1]['is_active'])
        self.assertFalse(menu_items[2]['is_active'])

        menu_items = get_menu_items('menu2', self.url3)
        self.assertEqual(len(menu_items), 2)
        self.assertEqual(menu_items[0]['title'], 'Menu 3')
        self.assertTrue(menu_items[0]['is_active'])

        menu_items = get_menu_items('menu2', self.url4)
        self.assertEqual(len(menu_items), 2)
        self.assertEqual(menu_items[0]['title'], 'Menu 3')
        self.assertFalse(menu_items[0]['is_active'])

    def test_render_menu(self):
        # Проверяем корректность рендеринга HTML-кода меню
        menu_items = get_menu_items('menu1', self.url1)
        menu_html = render_menu(menu_items)
        expected_html = '<ul><li class="active"><a href="/menu1/">Menu 1</a></li><li class=""><a href="/menu2/">Menu 2</a></li><li class=""><a href="/">Menu 5</a></li></ul>'
        self.assertHTMLEqual(menu_html, expected_html)

        menu_items = get_menu_items('menu2', self.url3)
        menu_html = render_menu(menu_items)
        expected_html = '<ul><li class="active"><a href="/menu3/">Menu 3</a><ul><li class=""><a href="/menu4/">Menu 4</a></li></ul></li><li class=""><a href="/menu4/">Menu 4</a></li></ul>'
        self.assertHTMLEqual(menu_html, expected_html)

        # Проверяем корректность рендеринга пустого меню
        menu_html = render_menu([])
        expected_html = ''
        self.assertHTMLEqual(menu_html, expected_html)

