import json
import requests

JSON_ADDR = 'https://rti-giken.jp/fhc/api/train_tetsudo/delay.json'

CHECK_LIST = [
    {
        'name': '中央･総武各駅停車',
        'company': 'JR東日本',
        'website': 'https://traininfo.jreast.co.jp/train_info/kanto.aspx'
    },
    {
        'name': '東西線',
        'company': '東京メトロ',
        'website': 'https://www.tokyometro.jp/unkou/history/touzai.html'
    },
]


def lambda_handler(event, context):

    notify_delays = get_notify_delays()

    if not notify_delays:
        return

    # Slack用のメッセージを作成して投げる
    (title, detail) = get_message(notify_delays)
    #post_slack(title, detail)

    print(title)
    print(detail)

    return


def get_notify_delays():

    current_delays = get_current_delays()

    notify_delays = []

    for delay_item in current_delays:
        for check_item in CHECK_LIST:
            if delay_item['name'] == check_item['name'] and delay_item['company'] == check_item['company']:
                notify_delays.append(check_item)

    return notify_delays


def get_current_delays():
    try:
        res = requests.get(JSON_ADDR)
    except requests.RequestException as e:
        print(e)
        raise e

    if res.status_code == 200:
        return json.loads(res.text)
    return []


def get_message(delays):
    title = "電車の遅延があります。"

    details = []

    for item in delays:
        company = item['company']
        name = item['name']
        website = item['website']
        details.append(f'・{company}： {name}： <{website}|こちら>')

    return title, '\n'.join(details)
