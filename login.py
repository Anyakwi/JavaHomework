#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from playwright.sync_api import sync_playwright
import json
import time


def login(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        try:
            page.goto("https://sso.bit.edu.cn/cas/login", wait_until="domcontentloaded", timeout=30000)
            
            try:
                page.wait_for_selector('app-root', state='attached', timeout=5000)
                page.wait_for_selector('input[name="username"], input[type="text"]', timeout=10000)
            except:
                print("等待超时")
            
            username_selector = 'input[name="username"]'
            page.fill(username_selector, username)
            
            password_selector = 'input[type="password"]'
            page.fill(password_selector, password)
            
            page.keyboard.press("Enter")
            
            login_success = False
            try:
                page.wait_for_url(lambda url: 'login' not in url.lower(), timeout=5000)
                login_success = True
            except:
                print("未检测到URL跳转")
            
            return login_success
            
        finally:
            browser.close()


def main():
    print("\n请输入登录信息:")
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
    
    success = login(username, password)
    
    if success:
        print(f"\n登录成功")
        return 0
    else:
        print(f"\n登录失败")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

