import network,time,_thread
from lib.microdot import Microdot,send_file,redirect

wifi_ssid = ""
wifi_pwd  = ""

def wifi_connect():
    global wifi_ssid,wifi_pwd
    if not wifi_ssid:
        print("[Wlan]未配置wifi")
        return False
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('[Wlan]开始尝试连接Wlan...')
        wlan.connect(wifi_ssid, wifi_pwd)
        times = 1
        while not wlan.isconnected():
            print(f"[Wlan][{times}]wlan try to connect...")
            times += 1
            time.sleep(0.5)
            if times > 10:
                print("[Wlan]密码ssid错误")
                wifi_ssid = ""
                wifi_pwd  = ""
                wlan.active(False)
                del wlan
                return False
    print(f'[Wlan]Connect success!\tIP:{wlan.ifconfig()[0]}', )
    wlan.active(False)
    del wlan
    return True

def wifi_scan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()

def create_AP():
    ap = network.WLAN(network.AP_IF)
    ap.config(authmode=0,essid="esp32",password="")
    ap.active(True)
    return ap

def start_configare_mode():
    print("[wifi_configare] 开启配网模式")
    ap = create_AP()
    
    app = Microdot()

    @app.route('/')
    async def index(request):
        return send_file("/public/index.html")

    @app.route('/scan')
    async def scan(request):
        wifiList = []
        for wifi in wifi_scan():
            wifiList.append(wifi[0].decode())
        return wifiList

    @app.route('/configareWifi',methods=["POST"])
    async def configWifi(request):
        global wifi_ssid,wifi_pwd
        print(request.form)
        wifi_ssid = request.form['ssid']
        wifi_pwd = request.form['pwd']
        if wifi_connect():
            return redirect("/shutdown")
        return "WiFi名称或者密码错误！"
    
    @app.route('/shutdown')
    async def shutdown(req):
        _thread.start_new_thread(lambda:(time.sleep(1),req.app.shutdown()),())
        return "WiFi连接成功！服务即将关闭..."
        
    app.run(port=80,debug=True)

def init():
    if not wifi_connect():
        start_configare_mode()

# init()
