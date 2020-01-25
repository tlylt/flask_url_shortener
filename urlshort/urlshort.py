from flask import render_template, request, redirect, url_for, flash,abort, session,jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

# blueprint stuff
bp = Blueprint('urlshort',__name__)

# register a url
@bp.route('/')
def home():
    # render_template looks for the file name in the templates folder
    # powered by Jinja
    return render_template('home.html',codes=session.keys())

# flask default only allows get request
@bp.route('/your-url', methods=['GET','POST']) #route and function name do not need to match
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/Liu Yongliang/Documents/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}
            
        # use urls.json to act as basic db
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']] = True
        # getting value from request
        # request.args is a dictionary
        return render_template('your_url.html',code=request.form['code'])

    else:
        # redirect if it is a GET request
        # url for will get the url for the function name
        return redirect(url_for('urlshort.home'))
    
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))