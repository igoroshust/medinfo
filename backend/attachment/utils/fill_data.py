import os
import sys
import django

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from datetime import date
from attachment.models import People, HistLpu, Lpu, T001, T007

# Очистка записей
HistLpu.objects.all().delete()
People.objects.all().delete()
T001.objects.all().delete()
T007.objects.all().delete()
Lpu.objects.all().delete()

# Заполнение LPU
lpu1 = Lpu.objects.create(code='750066', caption='ГУЗ Читинская ЦРБ', bossname='Емельянов Геннадий Константинович')
lpu2 = Lpu.objects.create(code='750145', caption='ГУЗ КМЦ', bossname='Рыкова Наталья Ивановна')
lpu3 = Lpu.objects.create(code='750144', caption='ГУЗ ДКМЦ', bossname='Нардина Ирина Владимировна')
lpu4 = Lpu.objects.create(code='750004', caption='ГУЗ КБ №3', bossname='Горяев Николай Ильич')
lpu5 = Lpu.objects.create(code='750001', caption='ГУЗ Краевая клиническая больница', bossname='Шальнев Виктор Александрович')

# Заполнение T001 (mcod — это ForeignKey на Lpu)
t001_1 = T001.objects.create(mcod=lpu1, nam_mo='Новотроицкая амбулатория', nom_podr='1')
t001_2 = T001.objects.create(mcod=lpu1, nam_mo='Участковая больница села Бургень', nom_podr='2')
t001_3 = T001.objects.create(mcod=lpu2, nam_mo='Поликлиническое подразделение №1', nom_podr='1')
t001_4 = T001.objects.create(mcod=lpu2, nam_mo='Поликлиническое подразделение №3', nom_podr='3')
t001_5 = T001.objects.create(mcod=lpu3, nam_mo='Поликлиническое подразделение №1', nom_podr='1')
t001_6 = T001.objects.create(mcod=lpu4, nam_mo="Поликлиника пгт.Первомайск", nom_podr='1')

# Заполнение T007 (code_mo — это ForeignKey на Lpu)
t007_1 = T007.objects.create(code_mo=lpu1, name_depth='Терапевтический участок', nom_podr='1', depth='1')
t007_2 = T007.objects.create(code_mo=lpu1, name_depth='Педиатрический участок', nom_podr='2', depth='2')
t007_3 = T007.objects.create(code_mo=lpu2, name_depth='Участок №1', nom_podr='1', depth='1')
t007_4 = T007.objects.create(code_mo=lpu2, name_depth='Участок №3', nom_podr='3', depth='3')
t007_5 = T007.objects.create(code_mo=lpu2, name_depth='Участок №10', nom_podr='3', depth='10')
t007_6 = T007.objects.create(code_mo=lpu3, name_depth='Участок №1', nom_podr='1', depth='2')
t007_7 = T007.objects.create(code_mo=lpu4, name_depth="Педиатрический участок №2", nom_podr='1', depth='4')

# Заполнение PEOPLE (lpu — ForeignKey на Lpu, lpuuch — ForeignKey на T007)
p1 = People.objects.create(enp='7594045746370284', fam='ИВАНОВ', im='ИВАН', ot='ИВАНОВИЧ', w=1, dr=date(1960,1,1))
p2 = People.objects.create(enp='7594045584245684', fam='ПЕТРОВ', im='ПЁТР', ot='ПЕТРОВИЧ', w=1, dr=date(1990,7,7), lpu=lpu2, lpudt=date(2020,1,1), lpudx=date(2020,7,1), lpuuch=t007_5)
p3 = People.objects.create(enp='7594045746375674', fam='СЕЛИНА', im='ЛЮБОВЬ', ot='ИЛЬИНИЧНА', w=2, dr=date(1968,5,4), lpu=lpu1)
p4 = People.objects.create(enp='7594045746370000', fam='ТОМСКИХ', im='ИРИНА', ot='СЕРГЕЕВНА', w=2, dr=date(2002,12,5), lpu=lpu2, lpudt=date(2020,1,1), lpuuch=t007_5)
p5 = People.objects.create(enp='7594029345746370', fam='ДОНДОКОВ', im='ТИМУР', ot='', w=1, dr=date(2018,2,16), lpu=lpu3, lpudt=date(2018,3,1), lpuuch=t007_6)

# Заполнение HISTLPU (lpu, district, subdiv — ForeignKey)
HistLpu.objects.create(pid=p2, lpu=lpu2, lpudt=date(2020,1,1), lpudx=date(2020,7,1), district=t001_3, subdiv=t007_3)
HistLpu.objects.create(pid=p3, lpu=lpu1, lpudt=None, lpudx=None, district=None, subdiv=None)
HistLpu.objects.create(pid=p4, lpu=lpu2, lpudt=date(2019,1,1), lpudx=date(2019,12,31), district=t001_4, subdiv=t007_4)
HistLpu.objects.create(pid=p4, lpu=lpu2, lpudt=date(2020,1,1), lpudx=None, district=t001_4, subdiv=t007_5)
HistLpu.objects.create(pid=p5, lpu=lpu3, lpudt=date(2018,3,1), lpudx=None, district=t001_5, subdiv=t007_6)

print('Данные загружены!')