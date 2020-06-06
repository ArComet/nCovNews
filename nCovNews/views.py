"""
Routes and views for the flask application.
"""
import time
import json
from datetime import datetime , date , timedelta
from flask import render_template,request,redirect,url_for,flash,session
from nCovNews import app , db
from nCovNews import datatype , data_predict , user_mod , forms , get_data 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    # 中国数据查询
    chinatotal = datatype.CHINATOTAL.query.order_by(datatype.CHINATOTAL.date.desc()).first()
    # 世界数据查询
    worldtotal = datatype.WORLDTOTAL.query.order_by(datatype.WORLDTOTAL.date.desc()).first()
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        chinatotal=chinatotal,
        worldtotal=worldtotal,
        message='Your home page.'
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/setphoto')
def setphoto():
    """Renders the contact page."""
    return render_template(
        'setphoto.html',
        title='Setphoto',
        year=datetime.now().year,
        message='Your setphoto page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/discuss',methods=['GET','POST'])
def discuss():
    """Renders the about page."""
    dislist = datatype.DISCUSS.query.filter_by(replyto=0).all()
    dislist.sort(key=lambda x:x.date,reverse=True)
    form = forms.PostForm()
    if form.validate_on_submit():
        id = session.get('userid')
        word = form.word.data
        user_mod.post_word(id,word)
        return  redirect(url_for('discuss'))
    return render_template(
        'discuss.html',
        title='Discuss',
        year=datetime.now().year,
        message='Your application description page.',
        dislist = dislist,
        form=form
    )

@app.route('/discuss_detail/<discussid>',methods=['GET','POST'])
def discuss_detail(discussid):
    """Renders the about page."""
    discuss = datatype.DISCUSS.query.filter_by(id=discussid).first()
    replylist = datatype.DISCUSS.query.filter_by(replyto=discussid).all()
    form = forms.PostForm()
    if form.validate_on_submit():
        id = session.get('userid')
        word = form.word.data
        user_mod.post_word(id,word,discussid)
        return  redirect(url_for('discuss_detail',discussid=discussid))
    return render_template(
        'discuss_detail.html',
        title='Detail',
        year=datetime.now().year,
        message='Your application description page.',
        discuss = discuss,
        replylist = replylist,
        form=form
    )

@app.route('/analyze')
def analyze():
    """Renders the about page."""
    return render_template(
        'analyze.html',
        title='Analyze',
        year=datetime.now().year,
        message='Your application description page.'
    )

from nCovNews.data_update import flags 

@app.route('/overview')
def overview():
    """Renders the home page."""
    today = date.today()
    oversea = datatype.COUNTRY.query.filter_by(date = today).all()
    return render_template(
        'overview.html',
        title='Overview',
        int = int,
        year=datetime.now().year,
        message='Your overview page.',
        oversea=oversea,
        flags=flags,
    )

@app.route('/news')
def news():
    """Renders the about page."""
    # 新闻数据查询
    news = datatype.NEWS.query.all()
    fakenews = datatype.FAKENEWS.query.all()
    information = datatype.INFORMATION.query.all()
    return render_template(
        'news.html',
        time = time,
        title='News',
        year=datetime.now().year,
        message='Your news page.',
        news=news,
        fakenews=fakenews,
        information=information,
        
    )

# 数据接口
@app.route('/getdata')
def getdata():
    return get_data.data()
    
@app.route('/delete_all_discuss')
def delete_all_discuss():
    user_mod.delete_all()
    return redirect(url_for('about'))

# 登陆表单
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        session['userid']=form.id.data
        session.permanent = True # 是否保存用户登录状态
        return redirect(url_for('home'))
    return render_template('login.html',
                           title='Login', 
                           form=form,)

@app.context_processor
def my_context_processor():
    userid = session.get('userid')
    user = datatype.USER.query.filter_by(userid=userid).first()
    if user:
        username = user.name
        return {'userid': userid,'username':username}
    return{}

# 登出
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 注册表单
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        dbsession = db.session
        user = datatype.USER(userid=form.id.data,name=form.name.data,password=form.password.data)
        dbsession.add(user)
        dbsession.commit()
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register', 
                           form=form, )

#没用的
@app.route('/test')
def test():
    """Renders the about page."""
    return render_template(
        'test.html',
        title='Test',
        year=datetime.now().year,
        message='Your test page.'
    )


