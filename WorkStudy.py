# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as BS


def login(username, password):
    sess = requests.session()
    sess.get("http://202.194.15.34:9000/login.do")
    if len(sess.post("http://202.194.15.34:9000/user.do?m=queryUser&username=%s" % username,
                     data="m=queryUser&username=%s" % username).text.split("y")) <= 0:
        print("用户未注册。")
        return None
    page = BS(sess.post("http://202.194.15.34:9000/j_acegi_login.do",
                        data={"j_username": username, "j_password": password}).text, "html.parser")
    div = page.find("body").find("div", {"align": "center"})
    if div:
        print(div.text.strip())
        return None
    return sess


def main(username, password, pid):
    sess = login(username, password)
    if sess:
        page = BS(sess.get("http://202.194.15.34:9000/xnqgzx.xn_dwzpxx.do?m=xssq&p_id=%s" % pid).text, "html.parser")
        print("确定岗位名称为“%s”吗？（n为取消，其他输入为确认）" % page.find("input", {"name": "p_gwmc"}).text.strip())
        if input() == "n":
            return
        dic = {}
        token = page.find_all("input")
        for i in token:
            if not i.attrs.get("name"):
                continue
            dic[i.attrs.get("name")] = i.attrs.get("value")
        text = sess.post("http://202.194.15.34:9000/xnqgzx.xn_sqb.do",
                         data=dic).text
        msg = text.split("showMsg(\"")[1].split("\"")[0]
        print(msg)


if __name__ == '__main__':
    main(input("用户名："), input("密码："), input("岗位号："))
