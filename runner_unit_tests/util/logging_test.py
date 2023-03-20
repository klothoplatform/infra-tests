import os
import pytest
from util import logging as runner_logging


def test_sibling_messages(be_github, grouped_logging_output):
    with runner_logging.grouped_logging('first'):
        grouped_logging_output.append('HELLO')
    with runner_logging.grouped_logging('second'):
        grouped_logging_output.append('WORLD')
    assert grouped_logging_output == [
            '::group::first',
            'HELLO',
            '::endgroup::',
            '::group::second',
            'WORLD',
            '::endgroup::',
    ]


def test_grouped_messages(be_github, grouped_logging_output):
    with runner_logging.grouped_logging('first'):
        grouped_logging_output.append('HELLO')
        with runner_logging.grouped_logging('second'):
            grouped_logging_output.append('WORLD')
            with runner_logging.grouped_logging('third'):
                grouped_logging_output.append('UNIVERSE!')
    assert grouped_logging_output == [
            '::group::first',
            'HELLO',
            '::endgroup::',
            '::group::first ❱ second',
            'WORLD',
            '::endgroup::',
            '::group::first ❱ second ❱ third',
            'UNIVERSE!',
            '::endgroup::',
    ]


def test_grouped__and_sibling_messages(be_github, grouped_logging_output):
    with runner_logging.grouped_logging('first'):
        grouped_logging_output.append('HELLO')
        with runner_logging.grouped_logging('second'):
            grouped_logging_output.append('WORLD')
        with runner_logging.grouped_logging('third'):
            grouped_logging_output.append('UNIVERSE!')
    assert grouped_logging_output == [
        '::group::first',
        'HELLO',
        '::endgroup::',
        '::group::first ❱ second',
        'WORLD',
        '::endgroup::',
        '::group::first ❱ third',
        'UNIVERSE!',
        '::endgroup::',
    ]


def test_exception_thrown(be_github, grouped_logging_output):
    for i in range(2):
        try:
            with runner_logging.grouped_logging(f'attempt {i}'):
                raise Exception("yo")
        except Exception as e:
            grouped_logging_output.append(f'caught exception during attempt {i}')
    assert grouped_logging_output == [
        '::group::attempt 0',
        '::endgroup::',
        'caught exception during attempt 0',  # note: this is _after_ the endgroup, since "with" was inside the "try"
        '::group::attempt 1',
        '::endgroup::',
        'caught exception during attempt 1',
    ]


@pytest.fixture
def be_github():
    old_value = os.environ.get('GITHUB_ACTIONS')
    os.environ['GITHUB_ACTIONS'] = 'true'
    yield
    if old_value is None:
        del os.environ['GITHUB_ACTIONS']
    else:
        os.environ['GITHUB_ACTIONS'] = old_value


@pytest.fixture
def grouped_logging_output():
    output: list[str] = []
    # noinspection PyProtectedMember
    old_output = runner_logging._grouped_logging_output
    runner_logging._grouped_logging_output = output.append

    yield output

    runner_logging._grouped_logging_output = old_output
