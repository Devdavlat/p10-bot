import csv
import os



class WriteCSV:
    def __init__(self, user_id, full_name, tasks):
        """"
        user_id - int
        full_name - str
        tasks - list
        """
        self.user_id = user_id
        self.first_name = full_name
        self.tasks = tasks

    @staticmethod
    def read_tasks_by_user_id(user_id):
        with open('tasks.csv', encoding='utf8') as file:
            print('read tasks is working')
            csv_reader = csv.DictReader(file)
            return [row.get('tasks') for row in csv_reader if row.get('user_id') == str(user_id)]

    def make_data(self):
        return [{
            'user_id': self.user_id,
            'full_name': self.first_name,
            'tasks': self.tasks
        }]

    def write_csv(self):
        header = ['user_id', 'full_name', 'tasks']
        data = self.make_data()
        with open('tasks.csv', 'a') as file:
            csv_writer = csv.DictWriter(file, header)
            if os.path.getsize('tasks.csv') == 0:
                csv_writer.writeheader()
            csv_writer.writerows(data)
        print('data saved successfully')

    @staticmethod
    def check_user_from_tasks_list(user_id):
        with open('tasks.csv', encoding='utf8') as file:
            print('check is working')
            csv_reader = csv.DictReader(file)
            return str(user_id) in [data.get('user_id') for data in csv_reader]

# task = WriteCSV(688964118, 'Davlatbek', 'Clean room')
# task.write_csv()

