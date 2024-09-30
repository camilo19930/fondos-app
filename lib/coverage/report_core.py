# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Reporter foundation for coverage.py."""

from __future__ import annotations

import sys

from typing import (
    Callable, Iterable, Iterator, IO, Protocol, TYPE_CHECKING,
)

from coverage.exceptions import NoDataError, NotPython
from coverage.files import prep_patterns, GlobMatcher
from coverage.misc import ensure_dir_for_file, file_be_gone
from coverage.plugin import FileReporter
from coverage.results import Analysis
from coverage.types import TMorf

if TYPE_CHECKING:
    from coverage import Coverage


class Reporter(Protocol):
    """What we expect of reporters."""

    report_type: str

    def report(self, morfs: Iterable[TMorf] | None, outfile: IO[str]) -> float:
        """Generate a report of `morfs`, written to `outfile`."""


def render_report(
    output_path: str,
    reporter: Reporter,
    morfs: Iterable[TMorf] | None,
    msgfn: Callable[[str], None],
) -> float:
    """Run a one-file report generator, managing the output file.

    This function ensures the output file is ready to be written to. Then writes
    the report to it. Then closes the file and cleans up.

    """
    file_to_close = None
    delete_file = False

    if output_path == "-":
        outfile = sys.stdout
    else:
        # Ensure that the output directory is created; done here because this
        # report pre-opens the output file.  HtmlReporter does this on its own
        # because its task is more complex, being multiple files.
        ensure_dir_for_file(output_path)
        outfile = open(output_path, "w", encoding="utf-8")
        file_to_close = outfile
        delete_file = True

    try:
        ret = reporter.report(morfs, outfile=outfile)
        if file_to_close is not None:
            msgfn(f"Wrote {reporter.report_type} to {output_path}")
        delete_file = False
        return ret
    finally:
        if file_to_close is not None:
            file_to_close.close()
            if delete_file:
                file_be_gone(output_path)           # pragma: part covered (doesn't return)


def get_analysis_to_report(
    coverage: Coverage,
    morfs: Iterable[TMorf] | None,
) -> Iterator[tuple[FileReporter, Analysis]]:
    """Get the files to report on.

    For each morf in `morfs`, if it should be reported on (based on the omit
    and include configuration options), yield a pair, the `FileReporter` and
    `Analysis` for the morf.

    """
    fr_morfs = coverage._get_file_reporters(morfs)
    config = coverage.config

    if config.report_include:
        matcher = GlobMatcher(prep_patterns(config.report_include), "report_include")
        fr_morfs = [(fr, morf) for (fr, morf) in fr_morfs if matcher.match(fr.filename)]

    if config.report_omit:
        matcher = GlobMatcher(prep_patterns(config.report_omit), "report_omit")
        fr_morfs = [(fr, morf) for (fr, morf) in fr_morfs if not matcher.match(fr.filename)]

    if not fr_morfs:
        raise NoDataError("No data to report.")

    for fr, morf in sorted(fr_morfs):
        try:
            analysis = coverage._analyze(morf)
        except NotPython:
            # Only report errors for .py files, and only if we didn't
            # explicitly suppress those errors.
            # NotPython is only raised by PythonFileReporter, which has a
            # should_be_python() method.
            if fr.should_be_python():       # type: ignore[attr-defined]
                if config.ignore_errors:
                    msg = f"Couldn't parse Python file '{fr.filename}'"
                    coverage._warn(msg, slug="couldnt-parse")
                else:
                    raise
        except Exception as exc:
            if config.ignore_errors:
                msg = f"Couldn't parse '{fr.filename}': {exc}".rstrip()
                coverage._warn(msg, slug="couldnt-parse")
            else:
                raise
        else:
            yield (fr, analysis)
