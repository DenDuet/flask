from flask import Flask, make_response, redirect, render_template, request, url_for

app = Flask(__name__)

context = {
    'name': ''
}


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/getcookie/')
def get_cookies():
    # получаем значение cookie
    name = request.cookies.get('username')
    return f"{name}"


@app.route('/pswd_form/', methods=['GET', 'POST'])
def pswd_form():
    if request.method == 'POST':
        auth_name = request.form.get('auth_name')
        auth_email = request.form.get('auth_email')

        context['name'] = auth_name

        if auth_name != "" and auth_email != "":
            response = make_response(
                render_template('deautoriz.html', **context))
            response.headers['new_head'] = 'New value'
            response.set_cookie('username', context['name'])
            return response
    return render_template('autoriz.html', **context)


@ app.route('/delcookie')
def delcookie():
    name = get_cookies()
    response = make_response(render_template(
        'autoriz.html', content=context))
    response.delete_cookie('username', name)
    context['name'] = ''

    return response


if __name__ == '__main__':
    app.run(debug=True)
