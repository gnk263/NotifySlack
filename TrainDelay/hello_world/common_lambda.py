import json
import requests

JSON_ADDR = 'https://rti-giken.jp/fhc/api/train_tetsudo/delay.json'


def get_notify_delays() -> list:
    """通知すべき遅延情報を取得する

    Returns:
        list: 通知すべき遅延情報
    """

    current_delays = get_current_delays()

    target_list = get_target_list()

    notify_delays = []

    for delay_item in current_delays:
        for check_item in target_list:
            if delay_item['name'] == check_item['name'] and delay_item['company'] == check_item['company']:
                notify_delays.append(check_item)

    return notify_delays


def get_target_list() -> list:
    """判定対象の路線情報を取得する

    Returns:
        list: 判定対象の路線情報
    """
    with open('target.json') as f:
        return json.load(f)


def get_current_delays() -> list:
    """
    現在の遅延情報を外部サイトから取得する
    Returns:
        list: 現在の遅延情報
    """
    try:
        res = requests.get(JSON_ADDR)
    except requests.RequestException as e:
        print(e)
        raise e

    if res.status_code == 200:
        return json.loads(res.text)
    return []


def get_message(delays) -> tuple:
    """Slackに通知するメッセージを作成する

    Args:
        delays: 通知すべき遅延情報

    Returns:
        str: メッセージのタイトル
        str: メッセージの詳細（遅延情報）
    """
    if not delays:
        return "電車の遅延はありません。", ""

    title = "電車の遅延があります。"

    details = []

    for item in delays:
        company = item['company']
        name = item['name']
        website = item['website']
        details.append(f'・{company}： {name}： <{website}|こちら>')

    return title, '\n'.join(details)
