import struct
import sys
import time
import socket
import threading
import re
import uuid
import random
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import paho.mqtt.client as mqtt
from kivy.clock import Clock
from datetime import datetime


# Thông số kết nối MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Tạo một BoxLayout để chứa TextInput cho tài khoản và nhập tài khoản
        UserName_layout = BoxLayout(
            orientation='horizontal', size_hint=(1, 0.1))

        # Tạo một TextInput cho tài khoản
        UserName_label = TextInput(
            text='Tài Khoản', readonly=True, size_hint=(0.3, 1))
        UserName_layout.add_widget(UserName_label)

        # Tạo một TextInput cho việc nhập tài khoản
        self.UserName_input = TextInput(text='admin', multiline=False)
        UserName_layout.add_widget(self.UserName_input)

        # Thêm UserName_layout vào layout chính
        layout.add_widget(UserName_layout)

        # Tạo một BoxLayout để chứa TextInput cho tài khoản và nhập mật khẩu
        Password_layout = BoxLayout(
            orientation='horizontal', size_hint=(1, 0.1))

        # Tạo một TextInput cho mật khẩu
        Password_label = TextInput(
            text='Mật Khẩu', readonly=True, size_hint=(0.3, 1))
        Password_layout.add_widget(Password_label)

        # Tạo một TextInput dùng cho việc nhập mật khẩu
        self.Password_input = TextInput(
            text='1', password=True, multiline=False)
        Password_layout.add_widget(self.Password_input)

        # Thêm Password_layout vào layout chính
        layout.add_widget(Password_layout)

        # Tạo một nút đăng nhập
        login_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        login_label = TextInput(readonly=True, background_color=(1, 1, 1, 1))
        login_layout.add_widget(login_label)

        login_button = Button(text='Đăng Nhập', size_hint=(0.3, 1))
        login_button.bind(on_press=self.login)
        login_layout.add_widget(login_button)

        layout.add_widget(login_layout)

        # Chèn 1 label vào để cân đối màn hình
        self.background_label = TextInput(
            readonly=True, background_color=(1, 1, 1, 1))
        layout.add_widget(self.background_label)

        self.add_widget(layout)

    def switch_to_main_screen(self, *args):
        App.get_running_app().root.current = 'main'

    def login(self, instance):
        UserName = self.UserName_input.text
        Password = self.Password_input.text
        mqtt_thread = threading.Thread(
            target=self.connect_and_login, args=(UserName, Password))
        mqtt_thread.start()

    def connect_and_login(self, UserName, Password):
        client = mqtt.Client()
        client_id = f'python-mqtt-{random.randint(0, 1000)}'

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker")
                client.subscribe(f"response/{client_id}")
                client.publish(
                    "user/login", json.dumps({"_id": client_id, "UserName": UserName, "Password": Password}))
            else:
                print("Failed to connect to MQTT Broker")
                self.background_label.text = "Failed to connect to MQTT Broker"

        def on_message(client, userdata, message):
            payload = message.payload.decode()
            data = json.loads(payload)
            result = data.get('value', '')
            if result == "OK":
                print("Login successful")
                Clock.schedule_once(self.switch_to_main_screen)
            else:
                print("Login unsuccessful. Please check your credentials!")
                self.background_label.text = "Login unsuccessful. Please check your credentials!"

        client.on_connect = on_connect
        client.on_message = on_message

        client_log = mqtt.Client()
        client_id_log = f'python-mqtt-{random.randint(0, 1000)}'

        def on_connect_log(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe(f"response/{client_id_log}")
                client.publish(
                    "device/get-device", json.dumps({"_id": client_id_log, "value": ""}))
            else:
                print("Failed to connect to MQTT Broker")

        def on_message_log(client, userdata, message):
            payload = message.payload.decode()
            data = json.loads(payload)
            data = data.get('value', '')
            App.get_running_app().root.get_screen('main').process_device_data(data)
        client_log.on_connect = on_connect_log
        client_log.on_message = on_message_log

        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        client_log.connect(MQTT_BROKER, MQTT_PORT, 60)
        client_log.loop_start()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Tạo một nút đăng xuất
        logout_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        refresh_button = Button(text='Refresh', size_hint=(0.3, 1))
        refresh_button.bind(on_press=self.refresh_data)
        logout_layout.add_widget(refresh_button)
        logout_label = Label(text='', size_hint=(0.4, 1))
        logout_layout.add_widget(logout_label)
        logout_button = Button(text='Đăng Xuất', size_hint=(0.3, 1))
        logout_button.bind(on_press=self.go_to_login)
        logout_layout.add_widget(logout_button)
        layout.add_widget(logout_layout)

        # Tạo một Label để hiển thị văn bản chào mừng
        self.welcome_label = Label(
            text='Danh sách thiết bị', size_hint=(1, 0.1))
        layout.add_widget(self.welcome_label)

        # Tạo một boxlayout
        self.table_layout = BoxLayout(
            orientation='vertical', size_hint=(1, 0.8))
        layout.add_widget(self.table_layout)

        self.add_widget(layout)

    def refresh_data(self, instance):
        client_log = mqtt.Client()
        client_id_log = f'python-mqtt-{random.randint(0, 1000)}'

        def on_connect_log(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe(f"response/{client_id_log}")
                client.publish(
                    "device/get-device", json.dumps({"_id": client_id_log, "value": ""}))
            else:
                print("Failed to connect to MQTT Broker")

        def on_message_log(client, userdata, message):
            payload = message.payload.decode()
            data = json.loads(payload) 
            data = data.get('value', '')
            print('Refesh successfull')
            self.process_device_data(data)

        client_log.on_connect = on_connect_log
        client_log.on_message = on_message_log
        client_log.connect(MQTT_BROKER, MQTT_PORT, 60)
        client_log.loop_start()

    def process_device_data(self, data):
        # Xử lý dữ liệu thiết bị nhận được từ MQTT
        # Lấy danh sách thiết bị từ dữ liệu MQTT và lưu trữ vào device_lst
        self.device_lst = data

        # Cập nhật giao diện sau khi nhận được danh sách thiết bị
        Clock.schedule_once(self.update_interface_with_devices)

    def update_interface_with_devices(self, *args):
        # Xóa tất cả các nút cũ trước khi tạo lại danh sách
        self.table_layout.clear_widgets()

        # Tạo lại danh sách nút từ device_lst mới nhất
        self.create_button_list(self.table_layout)

    def create_button_list(self, layout):
        pass
        for device in self.device_lst:
            button = Button(
                text=f'Thiết bị {device["Name"]}\n Khu vực: {device["DiaChi"]}', size_hint=(1, 1))
            button.bind(on_press=lambda btn,
                        val=device['value']: self.show_value(btn, val))
            layout.add_widget(button)

    def show_value(self, button, value):
        nhiet_do = value.get('T', 'N/A')
        do_am = value.get('H', 'N/A')
        timestr = value.get('time')
        # Chuyển đổi chuỗi thành đối tượng datetime
        time_object = datetime.fromisoformat(timestr)

        # Tách ngày và giờ
        date = time_object.date()
        time = time_object.time()

        formatted_value = f"Ngày: {date}\nThời gian: {time}\nNhiệt độ: {nhiet_do}°C\nĐộ ẩm: {do_am}%"
        popup = Popup(title='Thông tin thiết bị',
                      content=Label(text=formatted_value),
                      size_hint=(None, None), size=(800, 600))
       # Tạo nút "Back" và gán hàm xử lý sự kiện khi nhấn
        back_button = Button(text="Back", size_hint=(
            None, None), size=(100, 50))
    #     # Gán hàm xử lý sự kiện để đóng popup
        back_button.bind(on_press=popup.dismiss)

    #     # Thêm nút "Back" vào popup
        popup.content.add_widget(back_button)

     #     # Mở popup
        popup.open()

    def go_to_login(self, instance):
        App.get_running_app().root.current = 'login'


class ManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm


if __name__ == '__main__':
    ManagerApp().run()
