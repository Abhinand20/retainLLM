### RetainLLM: Retain everything you've ever read

#### Use cases


- Books: Generate and store quick summaries of each book chapter as you finish it. (natively support .epub e-books)
- Research papers: Insights and key takeaways from research papers.

#### Usage ideas

Support 2 top-level sub-commands

- book
    - summarize chapter(s)
    - interactive chat/discussion about chapter(s)

- article
    - summarize article
    - interactive discussion about section(s)

Basic usage for book:

- Parse a book and list chapters

```
retain.py book list --path=<epub_path>
```

- Summarize chapter(s)
```
retain.py book summarize --path=<epub_path> --start_chapter=<start_chapter> [--end_chapter=<end_chapter>] [--print] [--out_path=<output_path>]
```

- Interactive chat about chapter
```
retain.py book discuss --path=<epub_path> --start_chapter=<start_chapter> [--end=<end_chapter>] [--out_path=<output_path>]
```