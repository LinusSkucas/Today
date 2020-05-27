import json
from adapt.engine import IntentDeterminationEngine
from adapt.parser import Parser
from adapt.intent import IntentBuilder
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.trie import Trie
from adapt.tools.text.tokenizer import EnglishTokenizer
from enum import Enum

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()


class MessageIntent(Enum):
    ENROLL = "EnrollIntent"
    STOP = "StopIntent"
    OTHER = "Other"


enroll_keywords = [
    'start',
    'begin',
    'enroll',
    'enable'
]

stop_keywords = [
    'stop',
    'terminate',
    'end',
    'quit',
    'disable',
    'unenroll',
]

for enroll_keyword in enroll_keywords:
    engine.register_entity(enroll_keyword, "EnrollKeywords")

for stop_keyword in stop_keywords:
    engine.register_entity(stop_keyword, "StopKeywords")

enroll_intent = IntentBuilder(MessageIntent.ENROLL.value).require("EnrollKeywords").build()
stop_intent = IntentBuilder(MessageIntent.STOP.value).require("StopKeywords").build()

engine.register_intent_parser(enroll_intent)
engine.register_intent_parser(stop_intent)


def identify_message(message: str) -> MessageIntent:
    for intent in engine.determine_intent(utterance=message):
        if intent and intent.get('confidence') > 0:
            return MessageIntent(intent.get('intent_type'))
    return MessageIntent.OTHER
