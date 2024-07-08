from book_base import Book
from ebooklib import epub
import bs4
import epub_meta


class BookEPUB(Book):
    def __init__(self, book_path: str):
        super().__init__(book_path)
        try:
            self._book = self.get_book_obj(book_path)
            self._book_meta = self._get_metadata()
        except Exception as e:
            raise e
        
    def _get_metadata(self):
        return epub_meta.get_epub_metadata(self._path, read_cover_image = False)
    
    def _check_valid_index(self, index):
        toc = self._book_meta['toc']
        return index >= 0 and index < len(toc)
    
    def _remove_attribute_id(self, path):
        if '#' in path:
            path = path.split('#')[0]
        return path
    
    def get_chapter_title_from_index(self, index: int) -> str:
        toc = self._book_meta['toc']
        return toc[index]['title']
    
    def _get_content_between_files(self, src, index):
        tag_id = src.split('#')[-1]
        toc = self._book_meta['toc']
        chapter_src = self._remove_attribute_id(src)
        chapter_content = self._book.get_item_with_href(chapter_src)
        chapter_bs = bs4.BeautifulSoup(chapter_content.get_content())
        content = ""
        start_mark = chapter_bs.find(id=tag_id)
        if not start_mark:
            raise RuntimeError("Failed parsing book chapter")
        
        for tag in start_mark.next_elements:
            content += tag.get_text().strip()
        next_chapter_index = index + 1
        if self._check_valid_index(next_chapter_index):
            next_chapter_src = self._remove_attribute_id(toc[next_chapter_index]['src'])
            next_chapter_content = self._book.get_item_with_href(next_chapter_src)
            next_chapter_bs = bs4.BeautifulSoup(next_chapter_content.get_content())
            content += next_chapter_bs.get_text()
        
        return content
     
    def get_content(self, index: int, *args, **kwargs) -> str:
        toc = self._book_meta['toc']
        src = toc[index]['src']
        if src is None:
            return None
        if '#' in src:
            return self._get_content_between_files(src, index)
        # print(content_src)
        contentObj = self._book.get_item_with_href(src) 
        content = bs4.BeautifulSoup(contentObj.get_content())
        return content.get_text()
    
    def get_content_in_range(self, start: int, end: int, *args, **kwargs) -> tuple[str,int]:
        content = ''
        size = 0
        if (
            self._check_valid_index(start) and self._check_valid_index(end)
            and end >= start
        ):
            seen = set()
            toc = self._book_meta['toc']
            for i in range(start, end + 1):
                content_src = self._remove_attribute_id(toc[i]['src'])
                if content_src not in seen:
                    content += self.get_content(i) + '\n'
                    seen.add(content_src)
                    
            size = len(content)
            return content, size
        return content, size

    def get_toc(self):
        toc = self._book_meta['toc']
        toc_ret = []
        for item in toc:
            toc_ret.append((str(item['index']), item['title']))
        return toc_ret
         
    def get_book_obj(self, path: str):
        return epub.read_epub(path)
    
    def get_title(self) -> str:
        return self._book_meta['title']