# model_view_controller.py
from Shared_Power import sqlite_backend
from Shared_Power import mvc_exceptions as mvc_exc


class ModelSQLite(object):

    def __init__(self, application_items):
        self._item_type = 'users'
        self._connection = sqlite_backend.connect_to_db(sqlite_backend.DB_name)
        sqlite_backend.create_users_table(self.connection, self._item_type)
        self.create_items(application_items)

    @property
    def connection(self):
        return self._connection

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(
            self, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no):
        sqlite_backend.insert_one_users(
            self.connection, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no, table_name=self.item_type)

    def create_items(self, items):
        sqlite_backend.insert_users(
            self.connection, items, table_name=self.item_type)

    def read_item(self, usr_id):
        return sqlite_backend.select_one_users(
            self.connection, usr_id, table_name=self.item_type)

    def read_items(self):
        return sqlite_backend.select_all_users(
            self.connection, table_name=self.item_type)

    def update_item(
            self, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no):
        sqlite_backend.update_one_users(
            self.connection, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no, table_name=self.item_type)

    def delete_item(self, usr_id):
        sqlite_backend.delete_one_users(
            self.connection, usr_id, table_name=self.item_type)


class View(object):

    @staticmethod
    def show_bullet_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))

    @staticmethod
    def show_number_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

    @staticmethod
    def show_item(item_type, item, item_info):
        print('//////////////////////////////////////////////////////////////')
        print('Good news, we have some {}!'.format(item.upper()))
        print('{} INFO: {}'.format(item_type.upper(), item_info))
        print('//////////////////////////////////////////////////////////////')

    @staticmethod
    def display_missing_item_error(item, err):
        print('**************************************************************')
        print('We are sorry, we have no {}!'.format(item.upper()))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_already_stored_error(item, item_type, err):
        print('**************************************************************')
        print('Hey! We already have {} in our {} list!'
              .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_not_yet_stored_error(item, item_type, err):
        print('**************************************************************')
        print('We don\'t have any {} in our {} list. Please insert it first!'
              .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_stored(item, item_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Hooray! We have just added some {} to our {} list!'
              .format(item.upper(), item_type))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    @staticmethod
    def display_change_item_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change item type from "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_updated(
            item, o_pwrd, o_usr_type, o_first_name, o_last_name,
            o_add1, o_add2, o_add3, o_add4, o_post_code, o_tel_no,
            n_pwrd, n_usr_type, n_first_name, n_last_name,
            n_add1, n_add2, n_add3, n_add4, n_post_code, n_tel_no):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change {} '
              '\npwrd: {} --> {}'
              '\nusr_type: {} --> {}'
              '\nfirst_name: {} --> {}'
              '\nlast_name: {} --> {}'
              '\nadd1: {} --> {}'
              '\nadd2: {} --> {}'
              '\nadd3: {} --> {}'
              '\nadd4: {} --> {}'
              '\npost_code: {} --> {}'
              '\ntel_no: {} --> {}'
              .format(
                item, o_pwrd, n_pwrd, o_usr_type, n_usr_type,
                o_first_name, n_first_name, o_last_name, n_last_name,
                o_add1, n_add1, o_add2, n_add2, o_add3, n_add3, o_add4, n_add4,
                o_post_code, n_post_code, o_tel_no, n_tel_no))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_deletion(usr_id):
        print('--------------------------------------------------------------')
        print('We have just removed {} from our list'.format(usr_id))
        print('--------------------------------------------------------------')


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        items = self.model.read_items()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)

    def show_item(self, item_name):
        try:
            item = self.model.read_item(item_name)
            item_type = self.model.item_type
            self.view.show_item(item_type, item_name, item)
        except mvc_exc.ItemNotStored as e:
            self.view.display_missing_item_error(item_name, e)

    def insert_item(
            self, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no
    ):
        # assert price > 0, 'price must be greater than 0'
        # assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type
        try:
            self.model.create_item(
                usr_id, pwrd, usr_type, first_name, last_name,
                add1, add2, add3, add4, post_code, tel_no
            )
            self.view.display_item_stored(usr_id, item_type)
        except mvc_exc.ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(usr_id, item_type, e)

    def update_item(
            self, usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no
    ):
        # assert price > 0, 'price must be greater than 0'
        # assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type

        try:
            older = self.model.read_item(usr_id)
            self.model.update_item(
                usr_id, pwrd, usr_type, first_name, last_name,
                add1, add2, add3, add4, post_code, tel_no
            )
            self.view.display_item_updated(
                usr_id, older['pwrd'], older['usr_type'], older['first_name'], older['last_name'],
                older['add1'], older['add2'], older['add3'], older['add4'],
                older['post_code'], older['tel_no'],
                pwrd, usr_type, first_name, last_name, add1, add2, add3, add4, post_code, tel_no)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(usr_id, item_type, e)
            # if the item is not yet stored and we performed an update, we have
            # 2 options: do nothing or call insert_item to add it.
            # self.insert_item(name, price, quantity)

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        self.view.display_change_item_type(old_item_type, new_item_type)

    def delete_item(self, usr_id):
        item_type = self.model.item_type
        try:
            self.model.delete_item(usr_id)
            self.view.display_item_deletion(usr_id)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(usr_id, item_type, e)

if __name__ == '__main__':

    my_items = [
        {'usr_id': 'joebloggs', 'pwrd': 'secure', 'usr_type': 'Tool Owner',
         'first_name': 'Joe', 'last_name': 'Bloggs', 'add1': 'Putteridge Bury',
         'add2': 'Hitchin Rd', 'add3': 'Luton', 'add4': 'Bedfordshire',
         'post_code': 'LU2 8LE', 'tel_no': '01582 489069'},
        {'usr_id': 'john.smith', 'pwrd': 'password', 'usr_type': 'Tool User',
         'first_name': 'John', 'last_name': 'Smith', 'add1': 'Vicarage St',
         'add2': '', 'add3': 'Luton', 'add4': '',
         'post_code': 'LU1 3JU', 'tel_no': '01234 400400'},
        {'usr_id': 'admin', 'pwrd': 'admin', 'usr_type': 'Sys Admin',
         'first_name': 'System', 'last_name': 'Administrator', 'add1': '',
         'add2': '', 'add3': '', 'add4': '',
         'post_code': '', 'tel_no': ''},
    ]

    c = Controller(ModelSQLite(my_items), View())
    c.show_items()
    c.show_items(bullet_points=True)
    c.show_item('joebloggs')
    c.show_item('admin')

    c.insert_item(
        'joebloggs', pwrd='securepass', usr_type='Tool Owner', first_name='Joseph', last_name='Bloggs',
        add1='Putteridge Bury', add2='Hitchin Rd', add3='Luton', add4='Bedfordshire',
        post_code='LU2 8LE', tel_no='01582 489069')
    c.insert_item(
        'lukeskywalker', pwrd='jedi', usr_type='Tool User', first_name='Luke', last_name='Skywalker',
        add1='1 Star Wars Place', add2='Far Far Away', add3='Galaxy', add4='',
        post_code='SW1 8LJ', tel_no='01234 567890'
    )
    c.show_item('lukeskywalker')

    c.update_item(
        'joebloggs', pwrd='securepass', usr_type='Tool Owner', first_name='Joseph', last_name='Bloggs',
        add1='Putteridge Bury', add2='Hitchin Rd', add3='Luton', add4='Bedfordshire',
        post_code='LU2 8LE', tel_no='01582 489069')
    c.update_item(
        'admin2', pwrd='keepout', usr_type='Sys Admin', first_name='', last_name='',
        add1='', add2='', add3='', add4='',
        post_code='', tel_no='')

    c.delete_item('admin3')
    c.delete_item('admin3')

    c.show_items()

    # we close the current sqlite database connection explicitly
    if type(c.model) is ModelSQLite:
        sqlite_backend.disconnect_from_db(
            sqlite_backend.DB_name, c.model.connection)
        # the sqlite backend understands that it needs to open a new connection
        c.show_items()
