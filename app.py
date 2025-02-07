from flask import Flask, render_template, request, redirect, url_for, escape
from user import User
from utils import helper, get_weekwise, sing_or_plural, get_monthwise
app = Flask(__name__, static_url_path='/static')

app.debug = True
app.secret_key = "nothingfornow"


@app.route("/")
def home():
    args = dict(request.args)
    if 'q' in args:
        usr = User(args['q'])
        try:
            usr.get_details()
        except NameError:
            return render_template('index.html', data='Organization accounts \
                are not processed at the moment.')
        except:
            return render_template('index.html', data='Username not valid')
        else:
            return render_template('index.html', data=helper(usr))

    return render_template('index.html', data=None)


@app.route("/data", methods=['POST'])
def process():
    data = dict(request.form)
    usr = User(data['username'])
    # usr.get_details()
    try:
        usr.get_details()
    except NameError:
        return {'error': 'Organization accounts \
            are not processed at the moment.'}
    except:
        return {'error': 'Username not valid'}
    else:
        return {'value': helper(usr), 'days': get_weekwise(usr),
                'months': get_monthwise(usr)}


if __name__ == "__main__":
    app.run(port=5550)
