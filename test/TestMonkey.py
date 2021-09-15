# 一个monkey测试任务
import subprocess
import sys
import time

import tkinter as tk  # 装载tkinter模块,用于Python3

from test.DeviceCtrl import DeviceCtrl
from test.monkeytestcase import MonkeyTestCase


class TestMonkey(MonkeyTestCase):

    # setUp() 方法用于测试用例执行前初始化工作
    def setUp(self):
        pass

    # tearDown 测试用例执行之后的善后工作
    def tearDown(self):
        pass

    # 具体测试用例，必须test开头
    def test_monkey(self):

        try:
            logfilename = self.monkey_path + self.deviceid + '_monkey_' + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                                                    time.localtime()) + '.txt'
            screenpath = self.screen_save_path + self.deviceid + '_monkey_'

            devctrl = DeviceCtrl(self.deviceid)

            with open(logfilename, 'w', encoding='utf-8') as f:
                self.testcmd = self.monkeycmd
                self._testMethodDoc = self.story
                f.write(self.testcmd + '\r\n')
                ps = subprocess.Popen(self.testcmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
                rt = False
                reason = 'not run finished'
                while True:
                    line = ps.stdout.readline()
                    data = bytes.decode(line)
                    if data == '':
                        break
                    f.write(data)
                    self.logText.insert(tk.END, "\n"+data )
                    self.logText.see(tk.END)
                    if data.find('// Monkey finished') >= 0:
                        if reason == 'not run finished':
                            rt = True
                    elif data.find('** Monkey aborted due to error') >= 0:
                        rt = False
                        if reason == 'not run finished':
                            reason = 'Monkey aborted due to error'
                            logimagename = screenpath + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                      time.localtime()) + '_error_.png'
                            devctrl.screenshot(logimagename)
                    elif data.find('// CRASH:') >= 0:
                        rt = False
                        reason = data
                        logimagename = screenpath + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '_Crash.png'
                        devctrl.screenshot(logimagename)  # 出现失败截图
                    elif data.find('// NOT RESPONDING:') >= 0:
                        rt = False
                        reason = data
                        logimagename = screenpath + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '_ANR.png'
                        devctrl.screenshot(logimagename)  # 出现失败截图
                    elif data.find('New native crash detected') >= 0:
                        rt = False
                        reason = data
                        logimagename = screenpath + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                  time.localtime()) + '_NativeCrash.png'
                        devctrl.screenshot(logimagename)  # 出现失败截图

                ps.stdout.close()

                self.assertTrue(rt, reason)

        except Exception as e:

            self.assertTrue(False, e)