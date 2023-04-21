class Notification:
    def __init__(self, title: str, content: str, image_url: str):
        self.title = title
        self.content = content
        self.image_url = image_url

    def send(self):
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.__class__.__name__
