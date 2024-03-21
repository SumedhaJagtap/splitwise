class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = f'name:{user_id}'
        self.email = f'{user_id}@abc.com'
        self.phone_number = '1231231231'
