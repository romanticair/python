import random
import pyttsx3


class Person:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        self.engine = pyttsx3.init()
        self.engine.setProperty('name', name)
        self.engine.setProperty('gender', gender)
        self.engine.setProperty('age', age)
        self.set_speed_rate()
        self.set_volume()
        self.set_voice()
        self.onSpeak = False
        # 用于客户端给服务器转发
        self._msg = None

    def speak_to(self, name):
        self.onSpeak = True
        msg = input('write down the message you want to say to <{0}>:\n->'.format(name)).strip()
        if not msg:
            msg = '摁...'
        while self.onSpeak:
            # 每说一句话都更新
            self._msg = msg
            self.engine.say(msg)
            self.engine.runAndWait()
            msg = input('(Stop by quit or no)Anything else?\n->').strip()
            if msg.lower() in ['no', 'quit']:
                self.onSpeak = False
                self.engine.stop()

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    def set_speed_rate(self):
        rnd = random.randint(-100, 100)
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate + rnd)

    def set_volume(self):
        # 保留两位小数，整个范围 [-0.4, 0.5]
        rnd = round((random.randint(-4, 4) + random.random()) / 10, 2)
        # 默认 1
        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', volume + rnd)

    def set_voice(self):
        rnd = random.choice(self.engine.getProperty('voices'))
        self.engine.setProperty('voice', rnd)
