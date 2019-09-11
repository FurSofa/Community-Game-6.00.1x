class B:
    def __init__(self):
        self.val = 1

    def serialize(self):
        return self.__dict__

    @classmethod
    def deserialize(cls, s_data):
        dummy = cls()
        dummy.__dict__ = s_data.copy()
        return dummy


class A:
    def __init__(self):
        self.a = 0

    def serialize(self):
        s_dict = self.__dict__.copy()
        s_dict['b'] = self.b.serialize()
        return s_dict

    @classmethod
    def deserialize(cls, s_data):
        dummy = cls()
        dummy.__dict__ = s_data.copy()
        dummy.b = B.deserialize(s_data['b'])
        return dummy


a = A()
b = B()
a.b = b
data = a.serialize()
new_a = A.deserialize(data)
