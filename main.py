from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import requests

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.login)
        self.message_label = Label()

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.message_label)
        self.add_widget(self.layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        try:
            response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                self.manager.current = 'dashboard'
            else:
                self.message_label.text = response.json().get('message', 'Login failed. Please try again.')
        except requests.exceptions.RequestException as e:
            self.message_label.text = f'An error occurred: {str(e)}'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Welcome to the dashboard!')
        self.order_button = Button(text='Make Order')
        self.stats_button = Button(text='View Stats')
        self.filter_input = TextInput(hint_text='Filter Hamburgers')
        self.filter_button = Button(text='Filter')
        self.filter_button.bind(on_press=self.filter_hamburgers)
        self.filter_results = BoxLayout(orientation='vertical')

        self.order_button.bind(on_press=self.make_order)
        self.stats_button.bind(on_press=self.view_stats)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.order_button)
        self.layout.add_widget(self.stats_button)
        self.layout.add_widget(self.filter_input)
        self.layout.add_widget(self.filter_button)
        self.layout.add_widget(self.filter_results)
        self.add_widget(self.layout)

    def make_order(self, instance):
        self.manager.current = 'order'

    def view_stats(self, instance):
        self.manager.current = 'stats'

    def filter_hamburgers(self, instance):
        query = self.filter_input.text
        try:
            response = requests.get(f'http://127.0.0.1:5000/hamburgueres/search?query={query}')
            if response.status_code == 200:
                hamburgueres = response.json()
                self.filter_results.clear_widgets()
                for hamburguer in hamburgueres:
                    self.filter_results.add_widget(Label(text=hamburguer['nome_hamburguer']))
                    self.filter_results.add_widget(Label(text=hamburguer['ingredientes']))
                    img_path = f'../images/{hamburguer["imagem"]}'
                    self.filter_results.add_widget(Image(source=img_path))
            else:
                self.filter_results.add_widget(Label(text='Failed to retrieve hamburgers. Please try again.'))
        except requests.exceptions.RequestException as e:
            self.filter_results.add_widget(Label(text=f'An error occurred: {str(e)}'))

class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.client_id_input = TextInput(hint_text='Client ID')
        self.client_name_input = TextInput(hint_text='Client Name')
        self.client_address_input = TextInput(hint_text='Client Address')
        self.client_phone_input = TextInput(hint_text='Client Phone')
        self.hamburger_name_input = TextInput(hint_text='Hamburger Name')
        self.quantity_input = TextInput(hint_text='Quantity')
        self.size_input = TextInput(hint_text='Size (infantil, normal, duplo)')
        self.total_value_input = TextInput(hint_text='Total Value')
        self.order_button = Button(text='Submit Order')
        self.order_button.bind(on_press=self.submit_order)
        self.message_label = Label()

        self.layout.add_widget(self.client_id_input)
        self.layout.add_widget(self.client_name_input)
        self.layout.add_widget(self.client_address_input)
        self.layout.add_widget(self.client_phone_input)
        self.layout.add_widget(self.hamburger_name_input)
        self.layout.add_widget(self.quantity_input)
        self.layout.add_widget(self.size_input)
        self.layout.add_widget(self.total_value_input)
        self.layout.add_widget(self.order_button)
        self.layout.add_widget(self.message_label)
        self.add_widget(self.layout)

    def submit_order(self, instance):
        order_data = {
            'id_cliente': self.client_id_input.text,
            'nome_cliente': self.client_name_input.text,
            'morada_cliente': self.client_address_input.text,
            'telefone_cliente': self.client_phone_input.text,
            'nome_hamburguer': self.hamburger_name_input.text,
            'quantidade': self.quantity_input.text,
            'tamanho': self.size_input.text,
            'valor_total': self.total_value_input.text
        }
        try:
            response = requests.post('http://127.0.0.1:5000/pedidos', json=order_data)
            if response.status_code == 201:
                self.message_label.text = 'Order placed successfully!'
            else:
                self.message_label.text = response.json().get('message', 'Failed to place order. Please try again.')
        except requests.exceptions.RequestException as e:
            self.message_label.text = f'An error occurred: {str(e)}'

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.date_input = TextInput(hint_text='Date (YYYY-MM-DD)')
        self.view_button = Button(text='View Stats')
        self.view_button.bind(on_press=self.view_stats)
        self.results_label = Label()

        self.layout.add_widget(self.date_input)
        self.layout.add_widget(self.view_button)
        self.layout.add_widget(self.results_label)
        self.add_widget(self.layout)

    def view_stats(self, instance):
        date = self.date_input.text
        try:
            response = requests.get(f'http://127.0.0.1:5000/estatisticas?data={date}')
            if response.status_code == 200:
                stats = response.json()
                results_text = '\n'.join([f"Cliente: {stat['id_cliente']}, Hamburguer: {stat['nome_hamburguer']}, Quantidade: {stat['quantidade']}, Tamanho: {stat['tamanho']}, Valor: {stat['valor_total']}" for stat in stats])
                self.results_label.text = results_text
            else:
                self.results_label.text = response.json().get('message', 'Failed to retrieve stats. Please try again.')
        except requests.exceptions.RequestException as e:
            self.results_label.text = f'An error occurred: {str(e)}'

class CallCenterApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(DashboardScreen(name='dashboard'))
        self.screen_manager.add_widget(OrderScreen(name='order'))
        self.screen_manager.add_widget(StatsScreen(name='stats'))
        return self.screen_manager

if __name__ == '__main__':
    CallCenterApp().run()
