from youtube_transcript_api import YouTubeTranscriptApi
import utils
import json
import typer
import os
import os.path as osp
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from book_epub import BookEPUB
from model import Model
import prompts
import warnings
import pdfparser
warnings.filterwarnings('ignore')


def process_transcript(transcript):
   content = [t['text'] for t in transcript if t['text'].lower() != '[music]']
   normalized_text = " ".join(content)
   normalized_text = " ".join(normalized_text.split('\n'))
   return normalized_text

def extract_video_id(link):
    return link.split('?v=')[-1]

# with open('test_transcripts.json', 'w', encoding='utf-8') as json_file:
#     json_file.write(process_transcript(transcript))

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def summarize(yt_video_link: str, model_type: str = "mistral", save: bool = False):
    video_id = extract_video_id(yt_video_link)
    model = Model(model_type)
    utils.print_info(
        "generating summary of video with id '{}' using model [green]{}[/green] :fire:"
        .format(video_id, model.qualified_name)
        )
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        utils.print_error("could not fetch YT transcript: {}".format(e))
        return 
    content = process_transcript(transcript)
    resp = model.query(content[:20000], prompts.PODCAST_SUMMARY_PROMPT)
    console.print(Markdown(resp["generated_text"].strip()))
    # if save:
    #     out_dir = save_summary(OUT_DIR, resp['generated_text'].strip(), pdf_name, title)
    #     utils.print_info("saved summary in [green]{}[/green].".format(out_dir))

if __name__ == "__main__":
    app()