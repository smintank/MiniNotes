## Testing plan.

### Content:

1. ☑️ Заметки отсортированы от старой к новой. Свежие заметки в конце списка.
2. ☑️ Пользователь видит только свои заметки
3. ☑️ Авторизованный пользователь видит форму создания заметки

### Logic:

1. ☑️ Анонимный пользователь не может создать заметку. 
2. ☑️ Авторизованный пользователь может создать заметку.
3. Slag поле при создании заметки должно быть уникальным или показывать предупреждение
4. ☑️ Авторизованный пользователь может редактировать или удалять свои заметки.


### Routers:

1. ☑️ Главная страница доступна анонимному пользователю
2. ☑️ Страницы удаления и редактирования заметки доступны автору заметки
3. ☑️ Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям.
4. ☑️ При попытке перейти на страницу создания или списка заметок анонимный пользователь перенаправляется на страницу авторизации.