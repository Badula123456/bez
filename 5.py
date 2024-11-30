import os
import psutil
import json
import xml.etree.ElementTree as ET
import zipfile


def disk_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Точка монтирования: {partition.mountpoint}")
            print(f"Имя устройства: {partition.device}")
            print(f"Метка тома: {partition.opts}")
            print(f"Размер: {usage.total // (1024 ** 3)} ГБ")
            print(f"Тип файловой системы: {partition.fstype}")
            print("----------")
        except PermissionError:
            print(f"Нет доступа к разделу: {partition}")


class File:
    def __init__(self, filename):
        self.filename = filename

    def create_file(self):
        with open(self.filename, 'w') as f:
            print(f"Файл '{self.filename}' создан.")

    def write_to_file(self, content):
        with open(self.filename, 'a') as f:
            f.write(content + '\n')
            print(f"Записано в файл '{self.filename}': {content}")

    def read_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                content = f.read()
                print(f"Содержимое файла '{self.filename}':")
                print(content)
        else:
            print(f"Файл '{self.filename}' не найден.")

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Файл '{self.filename}' удален.")
        else:
            print(f"Файл '{self.filename}' не найден.")


class JsonFile:
    def __init__(self, filename):
        self.filename = filename

    def create_json_file(self):
        with open(self.filename, 'w') as f:
            json.dump({}, f)
            print(f"Файл '{self.filename}' создан.")

    def serialize_object(self, obj):
        with open(self.filename, 'w') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
            print(f"Объект записан в файл '{self.filename}'.")

    def read_json_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                content = json.load(f)
                print(f"Содержимое файла '{self.filename}':")
                print(json.dumps(content, ensure_ascii=False, indent=4))
        else:
            print(f"Файл '{self.filename}' не найден.")

    def delete_json_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Файл '{self.filename}' удален.")
        else:
            print(f"Файл '{self.filename}' не найден.")


class XmlFile:
    def __init__(self, filename):
        self.filename = filename

    def create_xml_file(self):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(self.filename)
        print(f"Файл '{self.filename}' создан.")

    def add_data_to_xml(self, tag, value):
        if os.path.exists(self.filename):
            tree = ET.parse(self.filename)
            root = tree.getroot()
            new_element = ET.SubElement(root, tag)
            new_element.text = value
            tree.write(self.filename)
            print(f"Добавлено: <{tag}>{value}</{tag}> в файл '{self.filename}'.")
        else:
            print(f"Файл '{self.filename}' не найден.")

    def read_xml_file(self):
        if os.path.exists(self.filename):
            tree = ET.parse(self.filename)
            root = tree.getroot()
            print(f"Содержимое файла '{self.filename}':")
            ET.dump(root)
        else:
            print(f"Файл '{self.filename}' не найден.")

    def delete_xml_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Файл '{self.filename}' удален.")
        else:
            print(f"Файл '{self.filename}' не найден.")


class ZipManager:
    def __init__(self, zip_filename):
        self.zip_filename = zip_filename

    def create_zip_archive(self):
        with zipfile.ZipFile(self.zip_filename, 'w') as zip_file:
            print(f"Создан архив '{self.zip_filename}'.")

    def add_file_to_zip(self, file_path):2
        if os.path.exists(file_path):
            with zipfile.ZipFile(self.zip_filename, 'a') as zip_file:
                zip_file.write(file_path, os.path.basename(file_path))
                print(f"Файл '{file_path}' добавлен в архив '{self.zip_filename}'.")
        else:
            print(f"Файл '{file_path}' не найден.")

    def extract_zip(self, max_size=1024**3):
        if os.path.exists(self.zip_filename):
            with zipfile.ZipFile(self.zip_filename, 'r') as zip_file:
                total_size = sum(zinfo.file_size for zinfo in zip_file.infolist())
                if total_size > max_size:
                    print(f"Ошибка: архив '{self.zip_filename}' слишком большой для распаковки "
                          f"(суммарный размер: {total_size / (1024**3):.2f} ГБ, лимит: {max_size / (1024**3):.2f} ГБ).")
                    return

                zip_file.extractall()
                print(f"Архив '{self.zip_filename}' распакован.")
                zip_file.printdir()
        else:
            print(f"Архив '{self.zip_filename}' не найден.")

    def delete_zip(self):
        if os.path.exists(self.zip_filename):
            os.remove(self.zip_filename)
            print(f"Архив '{self.zip_filename}' удален.")
        else:
            print(f"Архив '{self.zip_filename}' не найден.")



if __name__ == "__main__":
    while True:
        print("\nВыберите действие:")
        print("1. Просмотр информации о дисках")
        print("2. Работа с обычным файлом")
        print("3. Работа с JSON файлом")
        print("4. Работа с XML файлом")
        print("5. Работа с ZIP архивом")
        print("0. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            disk_info()
        elif choice == "2":
            filename = input("Введите имя файла: ")
            file = File(filename)
            action = input("1. Создать файл\n2. Записать в файл\n3. Прочитать файл\n4. Удалить файл\nВыберите действие: ")
            if action == "1":
                file.create_file()
            elif action == "2":
                content = input("Введите строку для записи: ")
                file.write_to_file(content)
            elif action == "3":
                file.read_file()
            elif action == "4":
                file.delete_file()
        elif choice == "3":
            filename = input("Введите имя JSON файла: ")
            json_file = JsonFile(filename)
            action = input("1. Создать JSON\n2. Записать объект\n3. Прочитать JSON\n4. Удалить JSON\nВыберите действие: ")
            if action == "1":
                json_file.create_json_file()
            elif action == "2":
                name = input("Введите имя: ")
                age = int(input("Введите возраст: "))
                obj = {"name": name, "age": age}
                json_file.serialize_object(obj)
            elif action == "3":
                json_file.read_json_file()
            elif action == "4":
                json_file.delete_json_file()
        elif choice == "4":
            filename = input("Введите имя XML файла: ")
            xml_file = XmlFile(filename)
            action = input("1. Создать XML\n2. Добавить данные\n3. Прочитать XML\n4. Удалить XML\nВыберите действие: ")
            if action == "1":
                xml_file.create_xml_file()
            elif action == "2":
                tag = input("Введите тег: ")
                value = input("Введите значение: ")
                xml_file.add_data_to_xml(tag, value)
            elif action == "3":
                xml_file.read_xml_file()
            elif action == "4":
                xml_file.delete_xml_file()
        elif choice == "5":
            zip_filename = input("Введите имя архива: ")
            zip_manager = ZipManager(zip_filename)
            action = input("1. Создать архив\n2. Добавить файл\n3. Распаковать архив\n4. Удалить архив\nВыберите действие: ")
            if action == "1":
                zip_manager.create_zip_archive()
            elif action == "2":
                file_to_add = input("Введите путь к файлу: ")
                zip_manager.add_file_to_zip(file_to_add)
            elif action == "3":
                zip_manager.extract_zip()
            elif action == "4":
                zip_manager.delete_zip()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Повторите попытку.")
