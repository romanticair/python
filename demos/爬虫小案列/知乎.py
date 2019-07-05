# 进入知乎的登录页面 
# 打开开发者工具(F12)，尝试输入错误并登录，观察浏览器是如何发送请求的
#
# 从请求中获取关键信息, 分析得到以下信息
# 实际登录的URL地址 https://www.zhihu.com/login/email
# 需要提供的表单数据有4个: 用户名(email)、密码(password)、验证码(captcha)、_xsrf
# 获取验证码的URL地址是 https://www.zhihu.com/captcha.gif?r=1490690391695&type=login
#
# _xsrf - CSRF(跨站请求伪造)攻击，xsrf是一串伪随机数，用于防止跨站请求伪造的
# 在页面上搜索 'xsrf'，知道其隐藏在一个 input 标签中，等下我们可以从里面获取该值


# http.cookiejar 模块可用于自动处理HTTP Cookie，LWPCookieJar 对象就是对 cookies 的
# 封装，它支持把 cookies 保存到文件以及从文件中加载
# 而 session 对象提供了 Cookie 的持久化，连接池功能，可以通过 session 对象发送请求
from http import cookiejar
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    # 首先从cookies.txt文件中加载cookie信息
    session.cookies.load(ignore_discard=True)
	# 因为首次运行还没有cookie，出现异常
except LoadError:
    print("load cookies failed")
	
def get_xsrf():
    """
    获取 xsrf
    """
    response = session.get("https://www.zhihu.com", headers=headers)
	# 利用 BeatifulSoup 的 find 方法可以非常便捷的获取该值
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf


def get_captcha():
    """
    把验证码图片保存到当前目录，人工手动识别验证码，
	也可以用第三方支持库来自动识别，比如 pytesser。
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha
	
def login(email, password):
    """
	登录接口，请求成功后，session会自动把 cookie 信息填充到 session.cookies对象，
	下次请求，客户端会自动携带这些cookie去访问需要登录的页面了。
	"""
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'}
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])
    for i in session.cookies:
        print(i)
    session.cookies.save()
