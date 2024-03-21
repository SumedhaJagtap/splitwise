import uuid


class IDGenerator:
    generated_ids = set()

    @classmethod
    def generate_unique_id(cls):
        while True:
            new_id = uuid.uuid4()
            if new_id not in cls.generated_ids:
                cls.generated_ids.add(new_id)
                return new_id
