from Data import History_info

class Log_In:
    def __init__(self):
        self.__Name = ""
        self.__ID = ""

    def enter_name_ID(self, name, user_id):
        self.__Name = name
        self.__ID = user_id

    def add_name_ID(self):
        History_info[self.__Name] = self.__ID

    def check_in_history(self):
        if self.__Name in History_info and History_info[self.__Name] == self.__ID:
            return True
        else:
            self.add_name_ID()
            return False

    def get_name(self):
        return self.__Name

    def get_id(self):
        return self.__ID