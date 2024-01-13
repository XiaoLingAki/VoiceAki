import openai
import requests
import time
import json
import sqlite3
import os

from loguru import logger
from session import ChatSessionManager_GLM as CM

model_list = ["gpt-3.5-turbo","gpt-4-0613"]
# openai.api_key = "sk-***"
# openai.api_base = "https://ngapi.xyz/v1"

session_manager = CM()

def chatgpt_pro(history):
    # print(openai.api_key)
    # print(type(history))
    logger.debug(history)
    logger.debug(openai.api_key)
    # openai.api_base = "http://localhost:8000/v1"
    # openai.api_key = "none"
    prompt_len = 0
    for h in history:
        print(h)
        prompt_len += len(h['content'])
        print(prompt_len)
    
    while prompt_len > 4399:
        prompt_len = prompt_len - len(history[1]['content'])
        history = [history[0]] + history[2:]
    
    # url = "https://localhost:8005/v1/chat/completions"
    # url = "https://api.openai-proxy.com/v1/chat/completions"
    url = "https://api.openai.com/v1/chat/completions"
    # url = "https://ngapi.xyz/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": history
    }
    time1 = time.time()
    response = requests.post(url, headers=headers, json=payload)
    time2 = time.time()
    if response.status_code == 200 or response.status_code == 202:
        completion = response.json()
        logger.debug(time2-time1)
        return completion["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def chatglm_pro(history):
    # print(openai.api_key)
    # print(type(history))
    logger.debug(history)
    logger.debug(openai.api_key)
    openai.api_base = "http://localhost:8003/v1"
    openai.api_key = "none"
    prompt_len = 0
    for h in history:
        print(h)
        prompt_len += len(h['content'])
        print(prompt_len)
    
    while prompt_len > 4399:
        prompt_len = prompt_len - len(history[1]['content'])
        history = [history[0]] + history[2:]
    
    url = "https://localhost:8003/v1/chat/completions"
    # url = "https://api.openai-proxy.com/v1/chat/completions"
    # url = "https://api.openai.com/v1/chat/completions"
    # url = "https://ngapi.xyz/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": history
    }
    time1 = time.time()
    response = requests.post(url, headers=headers, json=payload)
    time2 = time.time()
    if response.status_code == 200 or response.status_code == 202:
        completion = response.json()
        logger.debug(time2-time1)
        return completion["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def chatglm(prompt, history = []):
    url = "http://localhost:8005"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "history": history
    }
    # logger.debug(prompt)
    response = requests.post(url, headers=headers, json=data)
    logger.debug(response.text)
    response_data = json.loads(response.text)
    
    return response_data

def digital_person_chat(prompt = '', text = '你好', personality = "#粉毛", processer = "chatgpt"):
    
    logger.debug(text)
    chat_histories = session_manager.chat_histories

    if personality not in chat_histories:

        if processer == "chatgpt":
        # 如果当前prompt对应的history列表不存在，则创建一个新的空列表
            chat_histories[prompt] = [{"role": "system", "content": prompt}]
        else:
            chat_histories[personality] = prompt

    print('生成中……\n')
    try:
        if processer == "chatgpt":
            chat_histories[prompt].append({"role": "user", "content": text})
            # logger.debug(chat_histories[prompt])
            # logger.debug(prompt + history + text)
            result = chatgpt_pro(chat_histories[prompt])
        elif processer == "chatglm3":
            chat_histories[prompt].append({"role": "user", "content": text})
            # logger.debug(chat_histories[prompt])
            # logger.debug(prompt + history + text)
            result = chatglm_pro(chat_histories[prompt])
        else:
            ori_result = chatglm(text, history = chat_histories[personality])
            result = ori_result.get('response', '')
            history = ori_result.get('history', [])
            print(result)
            if len(history) > 20:
                history = history[0:2]
            print(history)
            chat_histories[personality] = history
            # print(chat_histories[prompt])
    except Exception as e:
        print(f"连接断开了喵！{e}")
        
    # result = "测试中~"
    return result


if __name__ == '__main__':
    # print(openai.api_key)
    # print(chatgpt_pro([
    # {"role": "system", "content": "You are a helpful assistant."},
    # {"role": "user", "content": "There are 9 birds in the tree, the hunter shoots one, how many birds are left in the tree？"}
    # ]))
    # print(openai.Model.list())
    print(digital_person_chat(text = input()))