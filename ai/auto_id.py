class AutoID:
    _id_counters = {}

    def __init__(self, **kwargs):
        class_name = self.__class__.__name__
        if class_name not in AutoID._id_counters:
            AutoID._id_counters[class_name] = 1
        if id not in kwargs or kwargs['id'] is None:
            self.id = AutoID._id_counters[class_name]
            AutoID._id_counters[class_name] += 1
        else:
            self.id = kwargs['id']

    @classmethod
    def reset_id_counters(cls):
        cls._id_counters = {}
