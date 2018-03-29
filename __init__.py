from monotonic import monotonic

from mycroft import MycroftSkill, intent_file_handler
from mycroft.version import CORE_VERSION_TUPLE


class RepeatRecentSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.last_stt = self.last_tts = None
        self.last_stt_time = 0

    def initialize(self):
        def on_utterance(message):
            self.last_stt = message.data['utterances'][0]
            self.last_stt_time = monotonic()

        def on_speak(message):
            self.last_tts = message.data['utterance']

        if CORE_VERSION_TUPLE >= (18, 2, 1):
            self.add_event('recognizer_loop:utterance', on_utterance)
            self.add_event('speak', on_speak)
        self.last_stt = self.last_tts = self.translate('nothing')

    @intent_file_handler('repeat.tts.intent')
    def handle_repeat_tts(self):
        self.speak_dialog('repeat.tts', dict(tts=self.last_tts))

    @intent_file_handler('repeat.stt.intent')
    def handle_repeat_stt(self):
        if monotonic() - self.last_stt_time > 120:
            self.speak_dialog('repeat.stt.old', dict(stt=self.last_stt))
        else:
            self.speak_dialog('repeat.stt', dict(stt=self.last_stt))

    @intent_file_handler('did.you.hear.me.intent')
    def handle_did_you_hear_me(self):
        if monotonic() - self.last_stt_time > 60:
            self.speak_dialog('did.not.hear')
            self.speak_dialog('please.repeat', expect_response=True)
        else:
            self.speak_dialog('did.hear')
            self.speak_dialog('repeat.stt', dict(stt=self.last_stt))


def create_skill():
    return RepeatRecentSkill()

