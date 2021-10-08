#!/usr/bin/env python3
import cgi
import sys
import codecs
import os
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
cookie_value = cookie.get("count_f")
if cookie_value is None: # якщо кукі не встановлено, тобто ми перший раз відкрили сторінку
    print(f"Set-cookie: count_f={1}")
    count_forms = 1
else:  # якщо сторінка відкривається повторно
    count_forms = int(cookie_value.value) + 1
    print(f"Set-cookie: count_f={count_forms}")

print("Content-type: text/html\r\n")
print() # This is mandatory !!!
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
form = cgi.FieldStorage()


lastname = form.getfirst("lastname", "не вказано")
firstname = form.getfirst("firstname", "не вказано")
if form.getvalue('expirience'):
   experience = form.getvalue('expirience')
else:
   experience = "не вибрано"
programming_language = form.getlist('prog_language')
print("""<!DOCTYPE HTML>
 <html>
 <head>
 <meta charset="utf-8">
 <title>Form Processing</title>
 </head>
 <body style='background-color:#CADABA;'>""")
print(f"""<div style='font-size:25px;position:relative; left:38%;'><b>Прізвище:</b>{lastname}<br>
<b>Ім'я:</b>{firstname}<br>
<b>Мови програмування:</b>""")
if len(programming_language) == 0:
    text = 'не вказано'
else:
    text = ''
    for elem in programming_language:
        text += elem+', '
    text = text[0:-2]
print(f"""{text}<br>
<b>OS:</b>{experience}<br>
<b>Кількість заповнених форм:</b>{count_forms}</div><br>
""")
print("<div style='position:relative; left:45%;'><a href='../index.html' style='font-size:30px'>Головна</a></div>")
print("""</body>
 </html>""")