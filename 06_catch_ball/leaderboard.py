from os import access, R_OK, W_OK, F_OK
import os.path


class Leaderboard:
    def __init__(self, filename='.rating.txt'):
        if not os.path.exists(filename):
            open(filename, 'w').close()

        if not (access(filename, R_OK) and access(filename, W_OK) and access(filename, F_OK)):
            raise Exception('File Mode Error')

        self.filename = filename
        self.file = open(filename, 'r')
        self.data = []
        self.read_data()
        self.sort_data()
        self.file.close()

    def read_data(self):
        line = self.file.readline()
        while line != '':
            name, rating = line.split(':')
            self.data.append([name, int(rating)])

            line = self.file.readline()

    def sort_data(self):
        self.data.sort(key=lambda x: x[1], reverse=True)

    def top_n(self, n):
        return self.data[:n:]

    def find_rating_by_name(self, search_name):
        for name, rating in self.data:
            if search_name == name:
                return name, rating

    def add_record(self, name, rating):
        for i in range(len(self.data)):
            if name == self.data[i][0]:
                self.data[i][1] = max(self.data[i][1], rating)
                return
        self.data.append((name, rating))
        self.sort_data()

    def save(self):
        file = open(self.filename, 'w')
        for (name, rating) in self.data:
            file.write('{name}:{rating}\n'.format(name=name, rating=rating))
        file.close()
