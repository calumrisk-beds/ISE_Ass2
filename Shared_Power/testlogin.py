"""
class ToolOwner:

    def __init__(self, id, pw, fname, lname):
        self.id = id
        self.pw = pw
        self.fname = fname
        self.lname = lname

    def return_tool_owner(self):
        return '\nID: {}'.format(self.id) + '\nFirst name: {}'.format(self.fname) + '\nLast name: {}'.format(self.lname)

    def return_id(self):
        return '{}'.format(self.id)

    def return_pw(self):
        return '{}'.format(self.pw)


class ToolUser:

    def __init__(self, id, pw, fname, lname):
        self.id = id
        self.pw = pw
        self.fname = fname
        self.lname = lname

    def return_tool_user(self):
        return '\nID: {}'.format(self.id) + '\nFirst name: {}'.format(self.fname) + '\nLast name: {}'.format(self.lname)


# Tool Owner
own1 = ToolOwner('1111', 'password', 'Mark', 'Smith')

# Tool Users
usr1 = ToolUser('2111', 'secure', 'Dan', 'Jones')

# print(own1.ReturnPW())

# Login

def login():
    id = input('Enter your ID: ')
    pw = input('Enter you password: ')

    if own1.return_id() == id and own1.return_pw() == pw:
        print('You are logged in!')
    else:
        print('Incorrect!')


login()
"""
