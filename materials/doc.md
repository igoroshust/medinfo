## Типы связей в Django
1. ForeignKey - многие к одному
Многие записи HistLpu могут ссылаться на одну People.
```python
class HistLpu(models.Model):
    pid = models.ForeignKey(People, on_delete=models.CASCADE, related_name='history')

# People(1) <- HistLpu (много)
# pid_id
```

- Обращение к записи People
```bash
hist.pid
```

- Обращение к истории People
```bash
people.history.all()
```

2. OneToOneField - один к одному
Одна запись связана только с одной другой записью
```python
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

# User (1) <- Profile (1)
```
- Профиль пользователя
```bash
user.profile
```

- Пользователь профиля
```bash
profile.user
```

3. ManyToManyField - многие ко многим
Многие записи могут ссылаться на многие другие
```python
class Student(models.Model):
    courses = models.ManyToManyField(Course, related_name='students')
# Student (Много) <- Course (много)
```
- Все курсы студента
```bash
student.courses.all()
```

- Все студенты курса
```bash
course.students.all()
```


## Механизм обратного связывания
При создании внешнего ключа
```python
class HistLpu(models.Model):
    pid = models.ForeignKey(People, related_name='history')
```

Джанго автоматически создаёт обратную связь
```bash
People (родитель) -> .history -> все HistLpu, связанные с этим People
```

**Пример:**
```python
# Модели
class People(models.Model):
    name = models.CharField(max_length=50)

class HistLpu(models.Model):
    pid = models.ForeignKey(People, on_delete=models.CASCADE, related_name='history')
```

```python
# Создание
person = People.objects.create(name='Иванов')
HistLpu.objects.create(pid=person, lpu='750001')
HistLpu.objects.create(pid=person, lpu='750002')

# Прямая связь (от дочернего к родителю)
hist = HistLpu.objects.first()
hist.pid.name  # 'Иванов'

# Обратная связь (от родителя к дочерним)
person = People.objects.first()
person.history.all()  # <QuerySet [...]>
```

Если не указывать `related_name`, Django использует имя модели с суффиксом `_set`:
```python
class HistLpu(models.Model):
    pid = models.ForeignKey(People, on_delete=models.CASCADE)

# Доступ через auto-generated имя
person.histlpu_set.all()  # автогенерируемое имя
```

Без `related_name` Django автоматически создаёт `modelname_set`.