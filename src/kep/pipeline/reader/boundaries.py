from typing import List
from kep.pipeline.parser.row_model import Row

class Boundary():
    def __init__(self, line, rows, name='boundary'):
        self.is_found = self.find(line, rows)
        self._name = name
        self._line = line

    def text(self):
        return self._line

    @staticmethod
    def find(line: str, rows: List[str]):
        for row in rows:
            if Row(row).startswith(line):
                return True
        return False

    def __str__(self):
        # FIXME: use %r
        def shorten(string):
            return f'<{string[:10]}...>'

        result = {True: 'found:  ', False: 'NOT found:'}[self.is_found]
        return f'{self._name} line {result} {shorten(self._line)}'


class Start(Boundary):
    def __init__(self, line, rows):
        super().__init__(line, rows, "Start")


class End(Boundary):
    def __init__(self, line, rows):
        super().__init__(line, rows, "End")


class Partition:
    def __init__(self, start: str, end: str, rows: List[List[str]]):
        self.start = Start(start, rows)
        self.end = End(end, rows)
        self.lines_count = len(rows)

    def is_matched(self) -> bool:
        return self.start.is_found and self.end.is_found

    def __str__(self):
        msg = [str(self.start),
               str(self.end),
               f'Total of {self.lines_count} rows']
        return '\n'.join(msg)


def get_boundaries(boundaries: List[dict], rows: List[str]):
    """Get start and end line, which is found in *rows* list of strings.

    Returns:
        start, end - tuple of start and end strings found in *rows*
    Raises:
        ValueError: no start/end line pairs was found in *rows*.
    """
    error_message = ['Start or end boundary not found:']
    for m in boundaries:
        partition = Partition(start=m['start'], end=m['end'], rows=rows)
        s, e = partition.start, partition.end
        if partition.is_matched():
            return s.text(), e.text()
        error_message.extend([str(s), str(e)])
    raise ValueError('\n'.join(error_message))