#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Time : 2017/11/1 ~ 2019/9/1
# @Author : Allen Woo
import base64
import os

from flask import render_template_string, render_template, g

from apps.configs.sys_config import TEMP_STATIC_FOLDER


def render_absolute_path_template(path, **context):
    """
    渲染绝对路径下template文件
    :param path:
    :param context:
    :return:
    """
    with open(path) as rhtml:
        source = rhtml.read()
    return render_template_string(source=source, **context)


def banel_translate_js_files(prefix, route_relative_path, absolute_path):

    if route_relative_path.endswith(".js"):
        # js 翻译
        name = os.path.split(route_relative_path)[-1]
        if "page_js" in route_relative_path or name.startswith("osr"):
            # 使用翻译好的js
            temp_name = "{}{}".format(route_relative_path, g.site_global["language"]["current"])
            temp_file_name = "{}_{}".format(prefix, base64.b16encode(temp_name.encode()).decode())
            absolute_path = "{}/{}.js".format(TEMP_STATIC_FOLDER, temp_file_name)
            if not os.path.isfile(absolute_path):
                with open(absolute_path, "w") as wf:
                    # flask中没找替换翻译js的Jinjia模块. 使用render_template来翻译js文件,
                    wf.write(render_template(route_relative_path))
            return absolute_path
    return absolute_path
