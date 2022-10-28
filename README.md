# Публикация комиксов XKCD во Вконтакте

Проект представляет собой скрипт, скачивающий комиксы с сайта [xkcd](https://xkcd.com).
После чего, выбранный случайным образом, комикс и комментарий к нему публикуется на стене в [группе VK](http://vk.com)

### Как установить

Для корректной работы вам понадобится указать в файле ```.env```:

- ACCESS_VK_TOKEN - получить его можно на [сайте для разработчиков VK](https://dev.vk.com)
- GROUP_ID - узнать id своей страницы можно [на данном сайте](https://regvk.com/id/) (убедитесь, что имеете все необходимые права для публикаций)

В итоге эти данные должны быть внесены в ```.env``` файл в таком виде:
```
ACCESS_VK_TOKEN=*токен вашего приложения*
GROUP_ID=*ID вашей группы/страницы на которую планируется постить*
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Запуск
Для публикации случайного комикса, введите в консоли:

```commandline
python main.py
```

 Пример работы программы:
 
 
![img_1.png](https://i.imgur.com/j62Tghy.jpg)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).