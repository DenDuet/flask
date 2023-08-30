# 📌 Создать базовый шаблон для интернет-магазина,
# содержащий общие элементы дизайна (шапка, меню,
# подвал), и дочерние шаблоны для страниц категорий
# товаров и отдельных товаров.
# 📌 Например, создать страницы "Одежда", "Обувь" и "Куртка",
# используя базовый шаблон.

from flask import Flask, render_template, request

app = Flask(__name__)

cat = [{'title': 'Картинка 1',
            'link': '0',
              'description': 'описание первой картинки',
              'img': '/static/images/pic1.jpg',
              },
             {'title': 'Картинка 2',
              'link': '1',
              'description': 'описание второй картинки',
              'img': '/static/images/pic2.jpg',
              }, 
             {'title': 'Картинка 3',
              'link': '2',
              'description': 'описание третьей картинки',
              'img': '/static/images/pic3.jpg',
              },     
             {'title': 'Картинка 4',
              'link': '3',
              'description': 'описание четвертой картинки',
              'img': '/static/images/pic4.jpg',
              },  
    ]

@app.route('/')
def main():
    return render_template('base.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
    selected_link = request.args.get('type')
    if (selected_link):
        context = {'cat': cat[int(selected_link)]}
        return render_template('cat.html', **context)
    
    return render_template('catalog.html', cat_block=cat)


if __name__ == '__main__':
    app.run(debug=True)
