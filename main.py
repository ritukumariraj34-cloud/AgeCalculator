from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.pickers.datepicker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import *
import datetime
from kivy.storage.jsonstore import JsonStore

KV = """
MDScreenManager:
    Screen:
        name:"s1"
        MDLabel:
            text:"Welcome"
            pos_hint:{"center_y":0.7,"center_x":0.76}
            font_style:"H4"
            bold:True
            italic:True
        MDLabel:
            text:"To"
            pos_hint:{"center_y":0.65,"center_x":0.93}
            font_style:"H5"
            bold:True
            italic:True
        MDLabel:
            text:"Age calculator"
            pos_hint:{"center_y":0.6,"center_x":0.66}
            font_style:"H4"
            bold:True
            italic:True
        MDFillRoundFlatIconButton:
            text:"Open"
            id:b
            pos_hint:{"center_x":0.5,"center_y":0.5}
            size_hint_x:0.5
            on_release:app.root.current="s2"
    Screen:
        name:"s2"
        MDBoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":1.42}
            MDTopAppBar:
                title:"Age calculator"
                right_action_items:[["information",lambda x:app.inform()]]
        MDFillRoundFlatIconButton:
            size_hint:(0.5,None)
            pos_hint:{"center_x":0.5,"center_y":0.8}
            text:"Date Of Birth"
            on_release: app.show_date_picker()
            id:cage
        MDFillRoundFlatIconButton:
            size_hint:(0.5,None)
            pos_hint:{"center_x":0.5,"center_y":0.73}
            text:"Current date"
            on_release: app.show_date_picker_calc()
            id:crd
        MDFillRoundFlatIconButton:
            text:"Calculate"
            pos_hint:{"center_x":0.5,"center_y":0.63}
            size_hint_x:0.5
            on_release: app.calculate_age()
        MDCard:
            elevation:3
            size_hint:(0.7, 0.2)
            pos_hint:{"center_x":0.5,"center_y":0.48}
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                MDLabel:
                    text:"Select dates to calculate"
                    halign: "center"
                    id:lb
                    font_style: "Subtitle1"
                MDLabel:
                    text:""
                    halign: "center"
                    id:nb_label
                    theme_text_color: "Secondary"
                    font_style: "Caption"
        MDFloatingActionButton:
            icon:"cog"
            pos_hint:{"center_x":0.83,"center_y":0.1}
            on_release:app.root.current="s3"
    Screen:
        name:"s3"
        MDBoxLayout:
            orientation:"vertical"
            pos_hint:{"center_x":0.5,"center_y":1.42}
            MDTopAppBar:
                title:"Setting"
        MDIconButton:
            icon:"arrow-left"
            pos_hint:{"center_x":0.1,"center_y":0.9625}
            on_release:app.root.current="s2"
        MDScrollView:
            pos_hint:{"center_y":0.41}
            MDList:
                OneLineListItem:
                    text:"dark mode"
                    id:oli
                    on_release:app.active()
                    MDSwitch:
                        pos_hint:{"center_x":0.85,"center_y":0.5}
                        widget_style:"ios"
                        id:sw
                        active:False
                        on_active: app.toggle_theme(self.active)
"""

class MyApp(MDApp):
    def build(self):
        self.icon = "icon.png" 
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Amber"
        self.store = JsonStore('settings.json')
        if self.store.exists('theme_setting'):
            theme_style = self.store.get('theme_setting')['style']
        else:
            theme_style = "Light"
        
        self.theme_cls.theme_style = theme_style
        self.dob_date = None
        self.calc_date = None
        self.app_root = Builder.load_string(KV)
        self.crage = self.app_root.ids.cage
        self.crdate = self.app_root.ids.crd
        self.result_label = self.app_root.ids.lb
        self.nb_label = self.app_root.ids.nb_label
        self.olitm=self.app_root.ids.oli
        self.switch=self.app_root.ids.sw
        self.switch.active = (self.theme_cls.theme_style == "Dark")
        return self.app_root

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_dob_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_dob_save(self, instance, value, date_range):
        self.dob_date = value
        self.crage.text = value.strftime("%B %d, %Y")

    def show_date_picker_calc(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_calc_date_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_calc_date_save(self, instance, value, date_range):
        self.calc_date = value
        self.crdate.text = value.strftime("%B %d, %Y")

    def on_cancel(self, instance, value):
        pass

    def show_dialog(self, text):
        dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        ,radius=[50,50,50,50])
        dialog.open()

    def calculate_age(self):
        if self.dob_date is None:
            self.show_dialog("Please select your date of birth.")
            return

        if self.calc_date is None:
            self.calc_date = datetime.date.today()

        if self.dob_date > self.calc_date:
            self.show_dialog("Date of birth cannot be after the calculation date.")
            return

        # 1. Exact Age Logic
        years = self.calc_date.year - self.dob_date.year
        months = self.calc_date.month - self.dob_date.month
        days = self.calc_date.day - self.dob_date.day

        if days < 0:
            months -= 1
            last_day_of_prev_month = self.calc_date.replace(day=1) - datetime.timedelta(days=1)
            days += last_day_of_prev_month.day

        if months < 0:
            years -= 1
            months += 12

        # 2. Next Birthday Logic
        today = datetime.date.today()
        next_bday = self.dob_date.replace(year=today.year)
        
        if next_bday <= today:
            next_bday = next_bday.replace(year=today.year + 1)
        
        days_to_bday = (next_bday - today).days

        # Update UI
        self.result_label.text = f"Age: {years}y, {months}m, {days}d"
        self.nb_label.text = f"Next Birthday in {days_to_bday} days"
    
    def active(self):
        self.switch.active = not self.switch.active
    
    def toggle_theme(self, is_active):
        if is_active:
            self.theme_cls.theme_style = "Dark"
            self.store.put('theme_setting', style="Dark")
        else:
            self.theme_cls.theme_style = "Light"
            self.store.put('theme_setting', style="Light")
    
    def inform(self):
        dialog = MDDialog(
            text="This is a simple Age Calculator",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss(),
                )
            ]
        ,radius=[50,50,50,50])
        dialog.open()

if __name__ == "__main__":
    MyApp().run()