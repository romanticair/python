"""
https://pyttsx3.readthedocs.io/en/latest/engine.html
字符串 -> 语音

下面从官方摘取了几个例子，进行了体验体验
语音阅读事件(阅读前，中，后，以及监听等事件)
语音阅读属性(语音，语速，语声)
"""
import pyttsx3

engine = pyttsx3.init()
# 可以提供驱动 默认驱动 win32配置的()，支持以下三个
# sapi5 - SAPI5 on Windows
# nsss - NSSpeechSynthesizer on Mac OS X
# espeak - eSpeak on every other platform
engine.say('I will speak this sentense. 嘤嘤嘤')
engine.say('Sally sells seashells by the seashore.')
engine.say('The quick brown fox jumped over the lazy dog.')


"""
# Listening for events
def onStart(name):
   print('starting', name)
def onWord(name, location, length):
   print('word', name, location, length)
def onEnd(name, completed):
   print('finishing', name, completed)
engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.')
"""

"""
# Interrupting an utterance
def onWord(name, location, length):
   print('word', name, location, length)
   if location > 10:
      engine.stop()
      
engine.connect('started-word', onWord)
engine.say('The quick brown fox jumped over the lazy dog.')
"""

"""
# Changing voices
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
"""


"""
# Changing speech rate and volume
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+50)
engine.say('The quick brown fox jumped over the lazy dog.')

volume = engine.getProperty('volume')
engine.setProperty('volume', volume-0.25)
engine.say('The quick brown fox jumped over the lazy dog.')
"""

engine.runAndWait()
