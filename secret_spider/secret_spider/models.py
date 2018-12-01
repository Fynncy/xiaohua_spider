# -*- coding: utf-8 -*-
# @Time         : 2018/11/30 17:25
# @Author       : sodalife
# @File         : models
# @Description  : 创建一个 mongoDB

import mongoengine


class IdorImage(mongoengine.Document):
    description = mongoengine.StringField()
    image = mongoengine.FileField()
