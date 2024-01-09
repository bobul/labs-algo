import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, \
    QTextBrowser


class SimpleDB:
    def __init__(self):
        self.records = []
        self.last_key = 0

    def binary_search(self, key):
        comparisons = 0
        start, end = 0, len(self.records) - 1

        while start <= end:
            mid = (start + end) // 2
            record_key, _ = self.records[mid]
            comparisons += 1

            print(f"Checking key {key} against record_key {record_key}")

            if record_key == key:
                return comparisons, self.records[mid]
            elif record_key < key:
                start = mid + 1
            else:
                end = mid - 1

        return comparisons, None

    def add_record(self, key, data):
        new_record = (key, data)
        self.records.append(new_record)
        self.records.sort()
        self.last_key = key

    def generate_incremental_data(self, num_records):
        for _ in range(num_records):
            key = self.last_key + 1
            data = f"Data for key {key}"
            self.add_record(key, data)

    def delete_record(self, key):
        for i, (record_key, _) in enumerate(self.records):
            if record_key == key:
                del self.records[i]
                break

    def edit_record(self, key, new_data):
        for i, (record_key, data) in enumerate(self.records):
            if record_key == key:
                self.records[i] = (key, new_data)
                break


class DBApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = SimpleDB()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.key_label = QLabel('Ключ:')
        self.key_input = QLineEdit(self)

        self.search_button = QPushButton('Пошук', self)
        self.search_button.clicked.connect(self.search_record)

        self.add_button = QPushButton('Додати', self)
        self.add_button.clicked.connect(self.add_record)

        self.delete_button = QPushButton('Видалити', self)
        self.delete_button.clicked.connect(self.delete_record)

        self.edit_button = QPushButton('Редагувати', self)
        self.edit_button.clicked.connect(self.edit_record)

        self.list_button = QPushButton('Список записів', self)
        self.list_button.clicked.connect(self.display_records)

        self.result_display = QTextBrowser(self)

        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.list_button)
        layout.addWidget(self.result_display)

        self.setCentralWidget(central_widget)
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Simple DB App')
        self.show()

    def search_record(self):
        key = int(self.key_input.text())
        total_comparisons = 0
        for _ in range(10):
            comparisons, result = self.db.binary_search(key)
            total_comparisons += comparisons

        average_comparisons = total_comparisons / 10
        if result:
            print(f"Record found: {result}")
            print(f"Average comparisons over 10 searches: {average_comparisons}")
        else:
            print("Record not found.")

        self.display_records()

    def add_record(self):
        self.db.generate_incremental_data(1)
        print(f"Record added: ({self.db.last_key}, 'Data for key {self.db.last_key}')")

    def delete_record(self):
        key = int(self.key_input.text())
        self.db.delete_record(key)
        print(f"Record with key {key} deleted.")

        self.display_records()

    def edit_record(self):
        key = int(self.key_input.text())
        new_data = f"New data for key {key}"
        self.db.edit_record(key, new_data)
        print(f"Record with key {key} edited to: {new_data}")

        self.display_records()

    def display_records(self):
        records_text = "List of Records:\n"
        for record_key, data in self.db.records:
            records_text += f"({record_key}, '{data}')\n"
        self.result_display.setPlainText(records_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBApp()

    db = ex.db
    db.generate_incremental_data(10000)

    sys.exit(app.exec_())
