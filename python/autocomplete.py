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

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        for i in range(5):
            yield Completion('completion' + str(math.floor(random.random()*10)), start_position=0)


#OOP version of global list history[]
class HistoryKeeper():
    def __init__(self) -> None:
        self.history = []

    def put_history(self, str):
        self.history.append(str)

    def get_history(self):
        # get this list from a file or secli session
        return self.history

class MySuggestion(AutoSuggest):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.historykeeper = kwargs["historykeeper"] if "historykeeper" in kwargs else None

    def get_suggestion(
        self, buffer: "Buffer", document: Document
    ) -> Optional[Suggestion]:
        history = self.historykeeper.get_history()

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

def main():
    historykeeper = HistoryKeeper()
    while True:
        text = prompt('> ', completer=MyCompleter(), auto_suggest=MySuggestion(historykeeper = historykeeper))
        historykeeper.put_history(text)
        if (text == "quit"):
            print("cli exit...")
            break
        print('You said: %s' % text)

if __name__ == '__main__':
    main()