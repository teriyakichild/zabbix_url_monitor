#!/usr/bin/python
# -*- coding: utf-8 -*-


class PidlockConflict(Exception):
    """
    Raised if an exclusive pid lock conflict exists
    """
    pass


class RquiredConfigMissing(Exception):
    """
    Raise if an expected config setting is undefined
    """
    pass


class AuthException(Exception):
    pass
