import os
import logging

LEVEL_MAP = {'DEBUG': logging.DEBUG,
             'INFO': logging.INFO,
             'WARNING': logging.WARNING,
             'ERROR': logging.ERROR,
             'CRITICAL': logging.CRITICAL}


def setup_loglevel():
    """環境変数からログレベルの設定を取得し、ルートロガーにセットする。
    環境変数に設定がない場合や、設定値に問題がある場合はなにもしない。
    """
    if 'LOG_LEVEL' not in os.environ:
        pass
    key = os.environ['LOG_LEVEL']
    if key in LEVEL_MAP:
        level = LEVEL_MAP[key]
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
