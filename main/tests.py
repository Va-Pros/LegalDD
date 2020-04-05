import sys
from django.test import TestCase, Client
from dictdiffer import diff
from main.models import *
import os
from LegalDD.settings import BASE_DIR, MEDIA_ROOT
from core.Parsing import parsing

class Parse_Test(TestCase):
    def parse_test_1(self):
        result = parsing('documents//test1.pdf')
        expected = {'Полное наименование': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ХАРБОР КЭПИТАЛ"',
                    'Сокращенное наименование': 'ООО "ХАРБОР КЭПИТАЛ"',
                    'Адрес': {'Почтовый индекс': '115191', 'Субъект Российской Федерации': 'ГОРОД МОСКВА',
                              'Улица (проспект, переулок и т.д.)': 'УЛИЦА РОЩИНСКАЯ 2-Я',
                              'Дом (владение и т.п.)': 'ДОМ 4', 'Офис (квартира и т.п.)': 'ПОМЕЩЕНИЕ 5 ЭТАЖ IА КОМ. 1'},
                    'ОГРН': '1177746582298', 'Дата регистрации': '13.06.2017', 'ИНН': '7725379244',
                    'Сведения об уставном капитале': {'Вид': 'УСТАВНЫЙ КАПИТАЛ', 'Размер': '10000', 'Дата внесения в ЕГРЮЛ':
                                                      '13.06.2017'},
                    'Сведения о директоре': {'Фамилия': 'ЗАКОШАНСКИЙ','Имя':'МИХАИЛ', 'Отчество': 'ВЛАДИМИРОВИЧ',
                                             'ИНН': '710601551255', 'Должность': 'ГЕНЕРАЛЬНЫЙ ДИРЕКТОР'},
                    'Сведения об учредителях': {1: {'Фамилия': 'ЗАКОШАНСКИЙ', 'Имя': 'МИХАИЛ', 'Отчество': 
                                                    'ВЛАДИМИРОВИЧ', 'ИНН': '7106015512', 'Номинальная стоимость доли': '5000'},
                                                2: {'Фамилия': 'ТОМАЕВ', 'Имя': 'ИНАЛ', 'Отчество': 'ОЛЕГОВИЧ',
                                                    'ИНН': '1516055255', 'Номинальная стоимость доли': '5000'}},
                    'Сведения об основном виде деятельности':
                    '70.22 Консультирование по вопросам коммерческой деятельности и управления'}
        differents = diff(expected, result)
        self.assertEqual(list(differents), [])
    def parse_test_2(self):
        result = parsing('..//Download Files//test2.pdf')
        expected = {'Полное наименование': 'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "РЕСПУБЛИКАНСКАЯ ФИНАНСОВАЯ КОРПОРАЦИЯ"',
                    'Сокращенное наименование': 'ОАО "РФК"', 'Адрес': {'Почтовый индекс': '107023', 'Субъект Российской Федерации': 'ГОРОД МОСКВА',
                                                                       'Улица (проспект, переулок и т.д.)': 'УЛИЦА СЕМЁНОВСКАЯ Б.', 'Дом (владение и т.п.)': '32',
                                                                       'Корпус (строение и т.п.)': 'СТР.1'}, 'ОГРН': '1097746360062', 'Дата регистрации': '19.06.2009',
                    'Сведения о прекращении': {'Способ прекращения':
                                               'Прекращение деятельности юридического лица в связи с его ликвидацией на основании определения арбитражного суда о завершении конкурсного производства', 'Дата прекращения': '31.10.2019'},
                    'ИНН': '7722688910', 'Сведения об уставном капитале': {'Вид': 'УСТАВНЫЙ КАПИТАЛ', 'Размер': '360400000', 'Дата внесения в ЕГРЮЛ': '19.06.2012'},
                    'Сведения о директоре': {'Фамилия': 'ЧЕРНЫЙ', 'Имя': 'МИХАИЛ', 'Отчество': 'ВАСИЛЬЕВИЧ', 'ИНН': '771900620884', 'Должность': 'КОНКУРСНЫЙ УПРАВЛЯЮЩИЙ'},
                    'Сведения о держателе реестра акционеров': {'ОГРН': '1077762194014', 'ИНН': '7722628904', 'Полное наименование': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "АВТОРУС-94"'},
                    'Сведения об учредителях': {1: {'ОГРН': '1077762194014', 'ИНН': '7722628904', 'Полное наименование': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "АВТОРУС-94"',
                                                    'Номинальная стоимость доли': '72000000'}, 2: {'ОГРН': '1027722003231', 'ИНН': '7722268627', 'Полное наименование':
                                                                                                   'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "ИНДУСТРИАЛЬНЫЙ АЛЬЯНС"', 'Номинальная стоимость доли':
                                                                                                   '49000000'}, 3: {'Фамилия': 'МАЛЬЧЕВСКИЙ', 'Имя': 'АНДЖЕЙ', 'Отчество': 'РЫШАРДОВИЧ',
                                                                                                                    'ИНН': '7703036472', 'Номинальная стоимость доли': '129000000'}},
                    'Сведения об основном виде деятельности': '64.9 Деятельность по предоставлению прочих финансовых услуг, кроме услуг по страхованию и пенсионному обеспечению'}
        differents = diff(expected, result)
        self.assertEqual(list(differents), [])
    def parse_test_3(self):
        result = parsing('..//Download Files//test3.pdf')
        expected = {'Полное наименование': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "УРАЛ"',
                  'Сокращенное наименование': 'ООО "УРАЛ"', 'Адрес': {'Почтовый индекс': '454046', 'Субъект Российской Федерации':
                                                                      'ОБЛАСТЬ ЧЕЛЯБИНСКАЯ', 'Город (волость и т.п.)':
                                                                      'ГОРОД ЧЕЛЯБИНСК', 'Улица (проспект, переулок и т.д.)':
                                                                      'УЛИЦА НОВОРОССИЙСКАЯ', 'Дом (владение и т.п.)': '122',
                                                                      'Офис (квартира и т.п.)': 'ОФИС 8 Б'},
                  'ОГРН': '1117449004859', 'Дата регистрации': '07.09.2011', 'Сведения о прекращении':
                  {'Способ прекращения':'Прекращение деятельности юридического лица путем реорганизации в форме слияния',
                   'Дата прекращения': '13.02.2013'}, 'ИНН': '7449105403', 'Сведения об уставном капитале':
                   {'Вид': 'УСТАВНЫЙ КАПИТАЛ', 'Размер': '10000', 'Дата внесения в ЕГРЮЛ': '07.09.2011'},
                   'Сведения о директоре': {'Фамилия': 'ЧЕРНОВА', 'Имя': 'ЯНА', 'Отчество': 'ВЯЧЕСЛАВОВНА',
                                            'ИНН': '745105565107', 'Должность': 'ДИРЕКТОР'},
                   'Сведения об учредителях': {1: {'Фамилия': 'ЧЕРНОВА', 'Имя': 'ЯНА', 'Отчество': 'ВЯЧЕСЛАВОВНА',
                                                   'ИНН': '7451055651', 'Номинальная стоимость доли': '10000'}},
                   'Сведения об основном виде деятельности':
                   '51.3 Оптовая торговля пищевыми продуктами, включая напитки, и табачными  изделиями'}
        differents = diff(expected, result)
        self.assertEqual(list(differents), [])
    def parse_test_4(self):
        result = parsing('..//Download Files//test4.pdf')
        expected = {'Полное наименование': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "УРАЛ"',
                    'Сокращенное наименование': 'ООО "УРАЛ"',
                    'Адрес': {'Почтовый индекс': '127486', 'Субъект Российской Федерации': 'ГОРОД МОСКВА',
                              'Улица (проспект, переулок и т.д.)': 'УЛИЦА ИВАНА СУСАНИНА', 'Дом (владение и т.п.)': 'ДОМ 2А',
                              'Офис (квартира и т.п.)': 'КОМНАТА 36'}, 'ОГРН': '5077746457058', 'Дата регистрации': '03.04.2007',
                    'ИНН': '7733602320',
                    'Сведения об уставном капитале': {'Вид': 'УСТАВНЫЙ КАПИТАЛ', 'Размер': '100000',
                                                      'Дата внесения в ЕГРЮЛ': '12.04.2017'},
                    'Сведения о директоре': {'Фамилия': 'ЛЕСНИКОВА', 'Имя': 'ЕЛЕНА', 'Отчество': 'ГЕОРГИЕВНА',
                                             'ИНН': '500900687252', 'Должность': 'ГЕНЕРАЛЬНЫЙ ДИРЕКТОР'},
                    'Сведения об учредителях': {1: {'Фамилия': 'ЛЕСНИКОВА', 'Имя': 'ЕЛЕНА', 'Отчество': 'ГЕОРГИЕВНА',
                                                    'ИНН': '5009006872', 'Номинальная стоимость доли': '100000'}},
                    'Сведения об основном виде деятельности': '46.90 Торговля оптовая неспециализированная'}
        differents = diff(expected, result)
        self.assertEqual(list(differents), [])

# Create your tests here.

users = dict()
profiles = dict()

def createUsers():
    # Обычный пользователь
    user = User.objects.create_user('reguser', password='regpassword')
    user.save()
    users['reguser'] = user
    profile = UserProfile(user=user)
    profile.is_lawyer = False
    profile.save()
    profiles['reguser'] = profile
    # Юрист
    user = User.objects.create_user('lawyer', password='lawpassword')
    user.save()
    users['lawyer'] = user
    profile = UserProfile(user=user)
    profile.is_lawyer = True
    profile.save()
    profiles['lawyer'] = profile
    # Админ
    user = User.objects.create_user('hseadmin', password='hsepassword')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    users['hseadmin'] = user
    profile = UserProfile(user=user)
    profile.is_lawyer = True
    profile.save()
    profiles['hseadmin'] = profile

class LoginTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()

    def testLoad(self):
        # Проверка GET запроса
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def testIncorrectForm(self):
        # Отправка некорректного запроса
        response = self.client.post('/accounts/login/')
        self.assertEqual(response.status_code, 400)

    def testIncorrectCredentials(self):
        # Попытка ввода неверной пары логин-пароль
        response = self.client.post('/accounts/login/', {'login': 'hacker', 'password': 'pass'})
        self.assertEqual(response.status_code, 400)

    def testRegular(self):
        # Попытка входа для пользователя reguser
        response = self.client.post('/accounts/login/', {'username': 'reguser', 'password': 'regpassword'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response.context['user'].user.username, 'reguser')

    def testLawyer(self):
        # Попытка входа для пользователя lawyer
        response = self.client.post('/accounts/login/', {'username': 'lawyer', 'password': 'lawpassword'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response.context['user'].user.username, 'lawyer')

    def testAdmin(self):
        # Попытка входа для пользователя hseadmin
        response = self.client.post('/accounts/login/', {'username': 'hseadmin', 'password': 'hsepassword'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response.context['user'].user.username, 'hseadmin')


class LogoutTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()
        
    def testLogout(self):
        self.client.force_login(users['reguser'])
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/accounts/login/')


class AdminTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()
        
    def testLoginReguser(self):
        # Попытка входа для пользователя reguser (пример не-администратора, не должен войти)
        self.client.force_login(users['reguser'])
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/admin/login/')
        
    def testLoginHseadmin(self):
        # Попытка входа для пользователя hseadmin (администратор, должен войти)
        self.client.force_login(users['hseadmin'])
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    # Остальной интерфейс администратора создан автоматически, его нет смысла тестировать

class LkTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()
        
    def testNoUser(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/accounts/login/')
    
    def testUser(self):
        self.client.force_login(users['reguser'])
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)   


class UploadTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()
        
    def tearDownClass():
        # Удалим загруженный файл
        os.remove(os.path.join(MEDIA_ROOT, 'runserver.bat'))

    def testNoUser(self):
        response = self.client.get('/upload/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/accounts/login/')
    
    def testUserGet(self):
        self.client.force_login(users['reguser'])
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 200)
    
    def testUploadEmpty(self):
        self.client.force_login(users['reguser'])
        response = self.client.post('/upload/')
        self.assertEqual(response.status_code, 400)
        
    def testUploadCorrect(self):
        self.client.force_login(users['reguser'])
        with open(os.path.join(BASE_DIR, 'runserver.bat'), 'r') as file:
            response = self.client.post('/upload/', {'file': file}, follow=True)
        self.assertURLEqual(response.request['PATH_INFO'], '/')
        file = Document.objects.get(file='runserver.bat')
        self.assertEqual(file.author, users['reguser'])
        self.assertEqual(file.content_type, 'text/plain')


class ProfileTest(TestCase):
    def setUp(self):
        createUsers()
        self.client = Client()
        self.rule = Rule(name='rule',
                    author=profiles['lawyer'])
        self.rule.save()
        self.profile = Profile(name='profile',
                               author=profiles['reguser'])
        self.profile.save()
        self.profile.rules.add(self.rule)
        self.profile.save()
    
    def testNoUser(self):
        response = self.client.get('/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/accounts/login/')
        
    def testReguser(self):
        self.client.force_login(users['reguser'])
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 403)
        
    def testLawyer(self):
        self.client.force_login(users['lawyer'])
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
    
    def testCreateProfileNoName(self):
        self.client.force_login(users['lawyer'])
        response = self.client.post('/profile/', {'rule_count':1, 'rule1':'rule'})
        self.assertEqual(response.status_code, 400)
        
    def testCreateProfileNoRuleCount(self):
        self.client.force_login(users['lawyer'])
        response = self.client.post('/profile/', {'name':'name'})
        self.assertEqual(response.status_code, 400)
        
    def testCreateProfileWrongRuleCount(self):
        self.client.force_login(users['lawyer'])
        response = self.client.post('/profile/', {'name':'name', 'rule_count':2, 'rule1':'rule'})
        self.assertEqual(response.status_code, 400)
    
    def testCreateProfile(self):
        self.client.force_login(users['lawyer'])
        response = self.client.post('/profile/', {'name':'name', 'rule_count':1, 'rule1':'rule'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], '/')
        
    def testEditProfileGet(self):
        self.client.force_login(users['lawyer'])
        response = self.client.get('/profile/', {'profile_id':self.profile.id})
        self.assertEqual(response.status_code, 200)
        
    def testEditProfileWrongId(self):
        self.client.force_login(users['lawyer'])
        response = self.client.post('/profile/', {'profile_id':-2, 'name':'name', 'rule_count':1, 'rule1':'rule'})
        self.assertEqual(response.status_code, 404)
