from google.cloud import speech
import types

from realtime_ai_character.audio.speech_to_text.base import SpeechToText
from realtime_ai_character.logger import get_logger
from realtime_ai_character.utils import Singleton

logger = get_logger(__name__)
config = types.SimpleNamespace(**{
    'encoding': speech.RecognitionConfig.AudioEncoding.LINEAR16,
    'sample_rate_hertz': 44100,
    'language_code': 'en-US',
    'max_alternatives': 1,
})


class Google(Singleton, SpeechToText):
    def __init__(self):
        super().__init__()
        logger.info("Setting up [Google Speech to Text]...")
        self.client = speech.SpeechClient()

    def transcribe(self, audio_bytes, platform, prompt='') -> str:
        batch_config = speech.RecognitionConfig({
            'speech_contexts': [speech.SpeechContext(phrases=prompt.split(','))],
            **config.__dict__})
        response = self.client.recognize(
            config=batch_config,
            audio=speech.RecognitionAudio(content=audio_bytes)
        )
        if not response.results:
            return ''
        result = response.results[0]
        if not result.alternatives:
            return ''
        return result.alternatives[0].transcript