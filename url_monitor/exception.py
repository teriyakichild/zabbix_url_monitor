#!/usr/bin/python
# -*- coding: utf-8 -*-


class UrlMonitorBaseException(Exception):
    """
    """
    pass


class PidlockConflict(UrlMonitorBaseException):
    """
    Raised if an exclusive pid lock conflict exists
    """
    pass


class RequiredConfigMissing(UrlMonitorBaseException):
    """
    Raise if an expected config setting is undefined
    """
    pass
