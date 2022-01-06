import random, math

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import Suggestion, AutoSuggest, AutoSuggestFromHistory
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer
from typing import Optional

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, NestedCompleter, Completer, Completion

ncompleter = NestedCompleter.from_nested_dict({
    'symdev': {
        '-sid': {
            'create': {
                '-num': None
            },
            'delete': {
                '-tar': None
            },
            'ip': {
                'interface': {'brief'}
            },
        },
    },
    'symclone': {},
    'symsnapvx': {},
    'symcfg': {},
    'symcli':{},
})

# text = prompt('# ', completer=ncompleter)
# print('You said: %s' % text)

# class MyCustomCompleter(Completer):
#     def get_completions(self, document, complete_event):
#         yield Completion('completion' + str(math.floor(random.random()*10)), start_position=0)

# text = prompt('> ', completer=MyCustomCompleter())

# session = PromptSession()

def gethistory():
    # get this list from a file or secli session
    return ["I have a dog", "my name is zzx", "I want to have a cat", "Hello world", "I want to have a dog"]

class mySuggestion(AutoSuggest):
    def get_suggestion(
        self, buffer: "Buffer", document: Document
    ) -> Optional[Suggestion]:
        history = gethistory()

        # Consider only the last line for the suggestion.
        text = document.text.rsplit("\n", 1)[-1]

        # Only create a suggestion when this is not an empty line.
        if text.strip():
            # Find first matching line in history.
            for string in reversed(history):
                for line in reversed(string.splitlines()):
                    if line.startswith(text):
                        return Suggestion(line[len(text) :])

        return None


while True:
    text = prompt('> ', completer = ncompleter ,auto_suggest=mySuggestion())
    print('You said: %s' % text)