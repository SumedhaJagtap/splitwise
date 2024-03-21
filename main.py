from splitwise import Splitwise


def process_command(splitwise_app, input_string):
    input_string = input_string.upper()
    parts = input_string.split()
    command = parts[0]
    if command == 'SHOW':
        user = parts[1] if len(parts) == 2 else None
        splitwise_app.show(user)
    else:
        payer = parts[1]
        amount_paid = float(parts[2])
        num_users = int(parts[3])

        users_involved = parts[4:4 + num_users]
        expense_type = parts[4 + num_users]

        if expense_type == "EQUAL":
            splitwise_app.add_expense(expense_type, payer, amount_paid, users_involved)
            return command, payer, amount_paid, num_users, users_involved, expense_type
        elif expense_type == "EXACT":
            exact_values = list(map(int, parts[5 + num_users:]))
            splitwise_app.add_expense(expense_type, payer, amount_paid, users_involved, exact_values)
            return command, payer, amount_paid, num_users, users_involved, expense_type, exact_values
        elif expense_type == "PERCENT":
            percentages = list(map(int, parts[5 + num_users:]))
            splitwise_app.add_expense(expense_type, payer, amount_paid, users_involved, percentages)
            return command, payer, amount_paid, num_users, users_involved, expense_type, percentages


if __name__ == '__main__':
    splitwise_app = Splitwise()
    while True:
        command = input('>')
        if command == 'EXIT':
            break
        process_command(splitwise_app, command)
