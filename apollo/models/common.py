#!/usr/bin/env python
#coding=utf-8


class Res():

    def __init__(self,code,message):
        self.code = code
        self.message = message

    def serialize(self):
        return {
            'code' : self.code,
            'message' : self.message
        }