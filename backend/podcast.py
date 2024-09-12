from youtube_transcript_api import YouTubeTranscriptApi
import utils
import typer
from rich.console import Console
from rich.markdown import Markdown
from model import model_factory
import prompts
import warnings
warnings.filterwarnings('ignore')


def process_transcript(transcript):
   content = [t['text'] for t in transcript if t['text'].lower() != '[music]']
   normalized_text = " ".join(content)
   normalized_text = " ".join(normalized_text.split('\n'))
   return normalized_text

def extract_video_id(link):
    return link.split('?v=')[-1]

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def summarize(yt_video_link: str, model_type: str = "gemini", save: bool = False):
    video_id = extract_video_id(yt_video_link)
    model = model_factory(model_type, prompts.PODCAST_SUMMARY_PROMPT)
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
    resp = model.query(content) 
    console.print(Markdown(resp.strip()))

if __name__ == "__main__":
    app()