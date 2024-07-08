from abc import ABC, abstractmethod

class Book(ABC):
    
    def __init__(self, book_path: str):
        self._path = book_path
    
    @abstractmethod
    def get_book_obj(self, path: str):
        pass
    
    @abstractmethod
    def get_toc(self):
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        pass
    
    @abstractmethod
    def get_content(self, *args, **kwargs) -> str:
        pass
    
    @abstractmethod
    def get_content_in_range(self, *args, **kwargs) -> str:
        pass