class Best_Whales:
    def __init__(self, capacity=0):  # Not used by default
        self.best_f_list = []
        self.whale_list = []
        self.capacity = capacity

    def add(self, best_f, whale):
        self.best_f_list.append(best_f)
        self.whale_list.append(whale)

        sorted_pairs = sorted(zip(self.best_f_list, self.whale_list), key=lambda x: x[0])

        if sorted_pairs:
            self.best_f_list, self.whale_list = map(list, zip(*sorted_pairs))
        else:
            self.best_f_list, self.whale_list = [], []

        if len(self.best_f_list) > self.capacity:
            self.best_f_list = self.best_f_list[:self.capacity]
            self.whale_list = self.whale_list[:self.capacity]

        # print(f'len_store: {len(self.best_f_list)}') # test

    def get_all(self):
        return list(zip(self.best_f_list, self.whale_list))

    def get_by_index(self, index):
        if 0 <= index < len(self.best_f_list):
            return self.best_f_list[index], self.whale_list[index]
        else:
            raise IndexError(f"current IndexError, {index}, {self.best_f_list}, {self.whale_list}")

    def size(self):
        return len(self.best_f_list)
