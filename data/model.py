class Client:
    id: int
    first_name: str
    last_name: str
    post_code: str
    city: str
    street: str
    building_number: int
    flat_number: int
    phone_number: str
    password: str
    last_update: int
    full: bool

    def __init__(self, first_name, last_name, post_code, city, street, building_number, flat_number, phone_number, password,
                 last_update=None, full=None, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.post_code = post_code
        self.city = city
        self.street = street
        self.building_number = building_number
        self.flat_number = flat_number
        self.phone_number = phone_number
        self.password = password
        self.last_update = last_update
        self.full = full

    def is_similar(self, text: str) -> bool:
        return self.first_name.lower().startswith(text) or self.last_name.lower().startswith(text)


class Storage:

    def __init__(self, max_id: int = 0):
        self.max_id = max_id
        self.client_set = set()

    def next_id(self) -> int:
        self.max_id += 1
        return self.max_id

    def get(self, id: int):
        if id is None:
            return None
        for entry in self.client_set:
            if entry.id == id:
                return entry
        return None

    def get_all(self) -> set:
        return self.client_set

    def add(self, entry: Client):
        self.max_id = max(entry.id, self.max_id)
        self.client_set.add(entry)

    def add_all(self, entry_set):
        if entry_set is None or len(entry_set) == 0:
            return
        self.max_id = max(self.max_id, max(entry_set, key=lambda client: client.id).id)
        self.client_set.update(self.client_set, entry_set)

    def remove(self, entry: Client):
        self.client_set.remove(entry)

    def clear(self):
        self.client_set.clear()
        self.max_id = 0

    def search_all(self, text: str) -> set:
        return self.search(text, self.client_set)

    @staticmethod
    def search(text: str, entry_set: set) -> set:
        if not text:
            return entry_set
        words = set(filter(lambda word: word, text.lower().split(" ")))
        return set(filter(lambda entry: entry.is_similar_all(words), entry_set))