# gpNeverErrorNew.py
'''
    iwebsns的测试模块
    如果驱动装在不同目录，请更改DRIVER参数指定的路径
    要发送到指定邮箱，请确认SMTP和POP3服务已经开启，推荐用qq邮箱，参数在REPORT里更改为自己的
    请务必确认HTMLTestRunner模块已经放在了Lib文件夹内，不然会报错，报告会自动生成在桌面
    被注释的代码是测试进程、线程、协程的东西，不用去管
    默认执行所有的一共11个测试用例
    随机邮箱测试用例偶尔可能重复注册，偶尔会跑Fail/概率极低，建议买彩票
    最后，祝你身体健康，再见
'''
__all__ = ('iwebsnsTest')  #可以导出的类
#全局变量
DRIVER = 'F:\Tools\\auto_Driver\chromedriver.exe'  # 驱动路径，自己更改
REPORT = {'mail':'731465297@qq.com',  #测试结果需要发送的邮箱地址信息
          'passwd':'bqfrppgvfbnfbcea',
          'host': 'smtp.qq.com',
          'port': '465'}
TEST_CASE = ('test_correctRegister_1',  #自定义导入需要测试的测试用例名称
            'test_correctRegister_2',
            'test_sameNameRegister',
            'test_correctLogin',
            'test_releaseLog',
            'test_checkAlbum',
            'test_checkPaper',
            'test_checkOnline',
            'test_seniorSearch',
            'test_clickHelp',
            'test_checkUserData')


import threading , unittest , time , random , string , yagmail
import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# from gevent import monkey
# from gevent.lock import Semaphore
from multiprocessing import Process

# monkey.patch_all()  #协程monkey

class iwebsnsTest(unittest.TestCase):     #声明测试用例类
    def setUp(self):
        URL = 'http://iwebsns.pansaifei.com'  # 定义URL
        self.iwebsns = webdriver.Chrome(DRIVER)
        self.iwebsns.get(URL)  # 进入被测网站
        self.iwebsns.implicitly_wait(10)  # 设置隐式等待时间
        self.iwebsns.maximize_window()  # 最大化窗口
        checks = self.iwebsns.find_elements_by_css_selector('[checked]')    #初始化把所有的状态都点掉
        for check in checks:
            check.click()
        # 进入主页

    def tearDown(self):
        sleep(0.5)
        self.iwebsns.quit()

    def test_correctRegister_1(self):
        u'正常的注册功能测试_1'
        #测试用例数据
        mail = ''.join(random.sample(string.ascii_letters+string.digits, 11)) + '@qq.com'  #生成随机邮箱
        print(mail)
        username = 'test1'
        passwd = '123456'
        sex = 1
        # 进入注册界面
        self.iwebsns.find_element_by_xpath('//span[@class="right"]/a[contains(@href,"reg")]').click()  #点击注册
        # 开始注册，输入注册数据
        self.register(self.iwebsns,mail,username,passwd)  #调用静态注册方法，输入参数
        sleep(1)
        self.assertTrue(username in self.iwebsns.title, msg='正常注册功能失败！')  # 断言判断是否注册成功

    def test_correctRegister_2(self):
        u'正常的注册功能测试_1'
        #测试用例数据
        mail = ''.join(random.sample(string.ascii_letters+string.digits , 11)) + '@qq.com'  #生成随机邮箱
        username = 'test2'
        passwd = '123456'
        sex = 0
        # 进入注册界面
        self.iwebsns.find_element_by_xpath('//span[@class="right"]/a[contains(@href,"reg")]').click()  #点击注册
        # 开始注册，输入注册数据
        self.register(self.iwebsns,mail,username,passwd,sex)  #调用静态注册方法，输入参数
        sleep(1)
        self.assertTrue(username in self.iwebsns.title, msg='正常注册功能失败！')  # 断言判断是否注册成功

    def test_sameNameRegister(self):
        u"邮箱相同注册流程测试"
        mail = 'aa@123.com'
        username = 'test2'
        passwd = '123456'
        sex = 1
        # 进入注册界面
        self.iwebsns.find_element_by_xpath('//span[@class="right"]/a[contains(@href,"reg")]').click()  # 点击注册
        # 开始注册，输入注册数据
        self.register(self.iwebsns, mail, username, passwd)  # 调用静态注册方法，输入参数
        sleep(1)
        msg = self.iwebsns.find_element_by_css_selector('#user_email_message').get_attribute('textContent')  # 抓取错误提示信息
        self.assertEqual(msg, '该email地址已存在，请重新输入', msg='错误提示信息错误！！')  # 判断信息是否一致

    def test_correctLogin(self):
        u'正常隐身登录测试'
        account = '731465297@qq.com'
        passwd = '123456'
        self.login(self.iwebsns,account,passwd,state = 'invisible')      #调用登录函数
        #断言判断是否正常隐身登陆
        sleep(1)
        self.assertTrue('个人首页' in self.iwebsns.title,msg = '没有成功登录！')
        self.iwebsns.switch_to.frame('frame_content')       #切换frame
        self.assertEqual(self.iwebsns.find_element_by_css_selector('#ol_label_txt').get_attribute('textContent'),'隐身',msg = '状态不是隐身！')      #断言判断隐身词缀

    def test_releaseLog(self):
        u'发布日志测试'
        account = '731465297@qq.com'
        passwd = '123456'
        content = '今天天气很好'
        self.login(self.iwebsns,account, passwd, state='invisible')  # 调用登录函数
        #发布日志
        self.iwebsns.find_element_by_css_selector('.app_blog>a').click()    #点击日志
        self.iwebsns.switch_to.frame('frame_content')
        self.iwebsns.find_element_by_css_selector('#iframecontent>div[class="create_button"]>a').click()       #点击新建日志
        self.iwebsns.find_element_by_css_selector('[name="blog_title"]').send_keys(content)         #输入标题
        self.iwebsns.switch_to.frame('KINDEDITORIFRAME')    #进入输入框

        self.iwebsns.find_element_by_css_selector('#KINDEDITORBODY').send_keys(content)         #输入内容
        self.iwebsns.switch_to.default_content()    #切换回操作的frame
        self.iwebsns.switch_to.frame('frame_content')
        sleep(1)
        self.iwebsns.find_element_by_css_selector('[type="submit"][class="regular-btn"]').click()       #点击确定提交
        #断言判断
        self.assertEqual(self.iwebsns.find_element_by_css_selector('.log_list:nth-of-type(1) strong>a').get_attribute('textContent'),content,msg = '标题保存错误！')
        self.assertEqual(self.iwebsns.find_element_by_css_selector('.log_list:nth-of-type(1) dt+dd').get_attribute('textContent'),content,msg = '内容保存错误！')

    def test_checkAlbum(self):
        u'测试查看相册功能'
        #登录
        account = '731465297@qq.com'
        passwd = '123456'
        self.login(self.iwebsns,account, passwd, state='invisible')  # 调用登录函数
        self.iwebsns.find_element_by_css_selector('.app_album>a').click()       #点击相册
        self.iwebsns.switch_to.frame('frame_content')       #切换frame
        #断言判断相册内容
        self.assertTrue(self.iwebsns.find_elements_by_css_selector('dl.list_album'),msg = '无法查看自己的相册内容或自己相册为空！')     #判断自己相册的内容
        #因为经常点不了好友相册，所以写了个循环判断一直点
        while str(self.iwebsns.find_element_by_css_selector('.active>a').get_attribute('textContent')) != '好友相册':   #判断是否点选了好友相册
            self.iwebsns.find_element_by_css_selector('ul.menu>li:nth-child(2)>a').click()     #点击好友相册查看
        sleep(1)
        self.assertTrue(self.iwebsns.find_elements_by_css_selector('dl.list_album'),msg = '无法查看好友的相册内容或好友相册为空！')     # 判断好友相册的内容

    def test_checkPaper(self):
        u'查看小纸条功能'
        account = '731465297@qq.com'
        passwd = '123456'
        self.login(self.iwebsns,account, passwd, state='invisible')  # 调用登录函数
        self.iwebsns.find_element_by_css_selector('dt>[href="main.php?app=msg_minbox"]').click()  # 点击小纸条
        self.iwebsns.switch_to.frame('frame_content')  # 切换frame
        #断言判断应该没有小纸条内容
        self.assertTrue(self.iwebsns.find_element_by_xpath('//div[@class="guide_info "][contains(text(),"对不起，您的收件箱内没有信息")]'),msg='信息提示错误或小纸条内已有消息！')

    def test_checkOnline(self):
        u'查看在线用户功能'
        account = '731465297@qq.com'
        passwd = '123456'
        self.login(self.iwebsns,account, passwd, state='invisible')  # 调用登录函数
        #查看在线好友
        self.iwebsns.find_element_by_css_selector('[href="modules.php?app=mypals_search_list&online=1"]').click()      #点击看谁在线
        self.iwebsns.switch_to.frame('frame_content')  # 切换frame
        #断言判断是否显示好友信息（如果有用户信息可以做匹配判断,这里只判断是显示用户的信息）
        self.assertTrue(self.iwebsns.find_elements_by_css_selector('div[class="pals_list"]'),msg='在线用户显示错误或没有查询到在线用户的信息！')

    def test_seniorSearch(self):
        u'高级搜索功能'
        account = '731465297@qq.com'
        passwd = '123456'
        searchUser = '857tt'
        self.login(self.iwebsns, account, passwd, state='invisible')  # 调用登录函数
        sleep(1)
        self.iwebsns.find_element_by_css_selector('.schbox+a').click()  #点击高级搜索
        self.iwebsns.switch_to.frame('frame_content')  # 切换frame
        self.iwebsns.find_element_by_css_selector('td>input[name="memName"]').send_keys('tt')  #输入搜索'tt'
        self.iwebsns.find_element_by_css_selector('.regular-btn').click()  #点击搜索
        sleep(1)
        #断言判断是否正确搜索到用户
        self.assertTrue(searchUser in self.iwebsns.find_element_by_css_selector('.pals_list>dl>dd:nth-child(1)').get_attribute('textContent'),msg='用户搜索错误或没有创建此用户！')

    def test_clickHelp(self):
        u'查看帮助功能'
        self.iwebsns.find_element_by_css_selector('[href="help/help.html"]').click()  #点击帮助
        #断言判断是否跳转到帮助界面
        self.assertTrue('帮助' in self.iwebsns.title,msg='没有正确跳转或网络出现错误！')

    def test_checkUserData(self):
        u'查看用户资料功能'
        account = '731465297@qq.com'
        passwd = '123456'
        username = 'Rainbird'
        self.login(self.iwebsns, account, passwd, state='invisible')  # 调用登录函数
        self.iwebsns.find_element_by_css_selector('div.left_nav a[href="home.php?h=9"]').click()  #点击我的主页
        self.iwebsns.find_element_by_css_selector('.menu>li:nth-of-type(2)>[href="javascript:void(0);"]').click()  #点击资料
        self.iwebsns.switch_to.frame('frame_content')  # 切换frame
        sleep(1)
        #断言判断资料是否正确
        self.assertEqual(self.iwebsns.find_element_by_css_selector('.form_table>tbody>tr:nth-of-type(1)>td').get_attribute('textContent'),username,msg='用户资料查看错误！')


        #内部静态方法，为测试用例服务，不是测试用例

    @staticmethod
    def register(iweb,mail,username,passwd,sex = 1,vcode = 'psf'):  #写个注册函数
        iweb.find_element_by_css_selector('#user_email').send_keys(mail)  # 输入邮箱
        iweb.find_element_by_css_selector('[name="user_name"]').send_keys(username)  # 输入用户名
        iweb.find_element_by_css_selector('#user_password').send_keys(passwd)  # 输入密码
        iweb.find_element_by_css_selector('#user_repassword').send_keys(passwd)  # 再次输入密码
        if sex == 1:
            iweb.find_element_by_css_selector('input[type="radio"]:nth-of-type(1)').click()  # 点击男性
        elif sex == 0:
            iweb.find_element_by_css_selector('input[type="radio"]:nth-of-type(2)').click()  # 点击女性
        iweb.find_element_by_css_selector('#veriCode').send_keys('{}\n'.format(vcode))  # 输入验证码
        iweb.find_element_by_css_selector('[value="注册"]').click()  # 点击注册

    @staticmethod
    def login(iweb,account,passwd,state = 'online'):    #写个登录函数
        iweb.find_element_by_css_selector('#login_email').send_keys(account)  # 输入账号
        iweb.find_element_by_css_selector('#login_pws').send_keys(passwd)  # 输入密码
        if state == 'invisible':
            iweb.find_element_by_css_selector('#hidden').click()  # 点选隐身
        iweb.find_element_by_css_selector('#loginsubm').click()  # 点击登录
        # 断言判断是否正常隐身登陆


def start(suite):    #跑测试的方法
    # lock.acquire()
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)   #开跑
    # lock.release()

    # 生成测试报告的代码，需要先安装HTMLTestRunner
    current_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())  # 字符串化当前时间
    filepath = 'C:/Users/hasee/Desktop/' + current_time + '_result.html'  #html报告路径
    file1 = open(filepath, mode="wb")  # 打开文件编辑html文件,以wb二进制方式打开
    reporter = HTMLTestRunner.HTMLTestRunner(stream=file1, title=u'GP 测试报告',description=u'iwebsns网站测试')  # 实例化runner，用HTML跑测试用例
    reporter.run(suite)
    file1.close()  # 关闭文件编辑

    #发送报告邮件
    yag = yagmail.SMTP(user=REPORT['mail'], password=REPORT['passwd'], host=REPORT['host'], port=REPORT['port'])
    contents = 'The reporter of the result for testing iwebsns at ' + current_time
    yag.send(to=REPORT['mail'], subject="Test's result for iwebsns at "+current_time, contents=contents,attachments=filepath)
    yag.close()

if __name__ == '__main__':
    suite = unittest.TestSuite()    #实例化需要测试的测试用例
    for case in TEST_CASE:
        suite.addTest(iwebsnsTest(case))
    start(suite)  #执行测试用例

    # #协程测试实现
    # name1 = '这是任务1111111111'
    # name2 = '这是任务2222222222'
    # sem = Semaphore(1)
    # lock = threading.RLock()
    # task1 = gevent.spawn(test,suite)
    # task2 = gevent.spawn(test,suite)
    #
    # gevent.joinall([task1,task2])

    # #进程实现
    # suite1 = unittest.TestSuite()
    # suite3 = unittest.TestSuite()
    # suite2 = unittest.TestSuite()
    # suite1.addTest(iwebsnsTest(TEST_CASE[0]))
    # suite1.addTest(iwebsnsTest(TEST_CASE[1]))
    # suite1.addTest(iwebsnsTest(TEST_CASE[2]))
    # suite2.addTest(iwebsnsTest(TEST_CASE[3]))
    # suite2.addTest(iwebsnsTest(TEST_CASE[4]))
    # suite2.addTest(iwebsnsTest(TEST_CASE[5]))
    # suite3.addTest(iwebsnsTest(TEST_CASE[6]))
    # suite3.addTest(iwebsnsTest(TEST_CASE[7]))
    # task1 = Process(target=test,args=(suite1,))
    # task2 = Process(target=test,args=(suite2,))
    # task3 = Process(target=test,args=(suite3,))
    # task1.start()
    # task2.start()
    # task3.start()
    # task1.join()
    # task2.join()
    # task3.join()

    print('测试结束')

