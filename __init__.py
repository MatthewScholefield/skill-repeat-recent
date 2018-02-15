from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler, intent_file_handler


class RepeatRecentSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.last_stt = self.last_tts = None

    def initialize(self):
        def on_utterance(_, message):
            self.last_stt = message.data['utterances'][0]

        def on_speak(_, message):
            self.last_tts = message.data['utterance']

        self.add_event('recognizer_loop:utterance', on_utterance, need_self=True)
        self.add_event('speak', on_speak, need_self=True)
        self.last_stt = self.last_tts = self.translate('nothing')

    @intent_file_handler('repeat.tts.intent')
    def handle_repeat_tts(self):
        self.speak_dialog('repeat.tts', dict(tts=self.last_tts))

    @intent_file_handler('repeat.stt.intent')
    def handle_repeat_stt(self):
        self.speak_dialog('repeat.stt', dict(stt=self.last_stt))


def create_skill():
    return RepeatRecentSkill()

