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
    'device': {
        '295': {
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
})

class IndexNavigator():
    def __init__(self, indexdoc) -> None:
        self.context = "" #string of the index document
        self.i       = 0  #cursor position in the document
        with open(indexdoc) as f:
            self.context = f.readlines()



class MyCompleter(Completer):
    def __init__(self, idx_nav) -> None:
        super().__init__()
        self.idx_nav = idx_nav
        
    def get_completions(self, document, complete_event):
#考虑每次根据doc新建nav还是一行命令用一个nav

        for i in range(5):
            yield Completion('completion' + str(math.floor(random.random()*10)), start_position=0)


#OOP version of global list history[]
class HistoryKeeper():
    def __init__(self) -> None:
        self.cmdhistory = []
        self.svrhistory = []
        self.devhistory = []

    def put_reshistory(self, res_type, s):
        if res_type == "svr":
            self.svrhistory.append(s)
        elif res_type == "dev":
            self.devhistory.append(s)
        else:
            print("error: res_type not support.")
    
    def get_reshistory(self, res_type):
        if res_type == "svr":
            return self.svrhistory
        elif res_type == "dev":
            return self.devhistory
        else:
            print("error: res_type not support.")

    def put_history(self, cmd):
        self.cmdhistory.append(cmd)

    def get_history(self):
        # get this list from a file or secli session
        return self.cmdhistory

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
    indexnav      = IndexNavigator("./doc/dev.ix")
    while True:
        text = prompt('> ', completer=MyCompleter(indexnav), auto_suggest=MySuggestion(historykeeper = historykeeper))
        historykeeper.put_history(text)
        if (text == "quit"):
            print("cli exit...")
            break
        print('You said: %s' % text)

if __name__ == '__main__':
    main()