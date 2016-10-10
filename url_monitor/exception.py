#!/usr/bin/python
# -*- coding: utf-8 -*-

class PidlockConflict(Exception):
    """
    Raised if an exclusive pid lock conflict exists
    """
    pass

class AuthException(Exception):
    pass
