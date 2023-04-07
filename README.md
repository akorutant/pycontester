# Сайт для конкурсов по Python
Итоговый проект в htmlacademy

паспорт проекта: https://docs.google.com/document/d/1vIgU5lKSHg4Yn4u2G2ot0JSs_7iL4Z9YxwQrsQ0WctA/edit?usp=sharing


сделаю типо коммит, чтоб была иллюзия работы
ТЗ:
1. Реализовать страницы сайта:
  1.1 Главная,
  1.2 Авторизация,
  1.3 Регистрация,
  1.4 Страница с соревнованиями,
  1.5 Страница с интерпритатором Python прямо в браузре.
  
2. База данных с таблицами:
  2.1 Users с полями: id, login, firstname, surname, patronymic, job_title, email, hashed_password, created_date,
  2.2 Teachers с полями: id, user_id,
  2.3 Contests с полями: id, title, description,
  2.4 Answers с полями: id, contest_id, true_answer.
  
3. При помощи микрофреймворка Flask реализовать сайт и его работоспособность:
  1. Регистрация и авторизация пользователей,
  2. Интерпритатора Python в брузере, а также автоматическя проверка решений пользователя при помощи ответов из таблицы базы answers,
  
