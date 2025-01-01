import time
import http.client
import json

# 配置部分
SERVER_HOST = "localhost"
SERVER_PORT = 53234
KEYWORDS = ["测试", "关键字2", "关键字3"]  # 替换为实际关键词
DEFAULT_REASON = "加群成功！"  # 默认的加群理由
BAN_DURATION = 60  # 禁言时间（秒）
POLLING_INTERVAL = 5  # 轮询时间间隔（秒）
group_id = 805950688


# 功能：获取群系统消息
def get_group_system_messages():
    conn = http.client.HTTPSConnection(SERVER_HOST, SERVER_PORT)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("GET", "/get_group_system_msg", headers=headers)
    res = conn.getresponse()
    data = res.read()
    try:
        messages = json.loads(data.decode("utf-8"))
        print("获取到的群系统消息:", messages)
        return messages
    except json.JSONDecodeError:
        print("获取群系统消息失败，返回数据:", data.decode("utf-8"))
        return {}


# 功能：处理加群请求
def handle_group_request(requester_uin, group_id, flag, message):
    # 检查关键词
    if any(keyword in message for keyword in KEYWORDS):
        print("检测到关键词，自动通过加群请求。")
        approve_group_request(flag, True, DEFAULT_REASON)  # 自动通过
        ban_user_in_group(group_id, requester_uin, BAN_DURATION)  # 禁言 1 分钟
        send_group_message(group_id, [
            {
                "type": "at",
                "data": {
                    "qq": requester_uin
                }
            },
            {
                "type": "text",
                "data": {
                    "text": f" 欢迎加入群聊！请先查看群公告和 Wiki。"
                }
            }
        ])
    else:
        print("未检测到关键词，拒绝加群请求。")
        approve_group_request(flag, False, "未符合加群要求。")


# 功能：通过或拒绝加群请求
def approve_group_request(flag, approve, reason):
    conn = http.client.HTTPSConnection(SERVER_HOST, SERVER_PORT)
    payload = json.dumps({
        "flag": flag,
        "approve": approve,
        "reason": reason
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/set_group_add_request", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print("加群请求处理结果:", data.decode("utf-8"))


# 功能：禁言群成员
def ban_user_in_group(group_id, user_id, duration):
    conn = http.client.HTTPSConnection(SERVER_HOST, SERVER_PORT)
    payload = json.dumps({
        "group_id": group_id,
        "user_id": user_id,
        "duration": duration
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/set_group_ban", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print("禁言操作结果:", data.decode("utf-8"))


# 功能：发送群消息
def send_group_message(group_id, message):
    conn = http.client.HTTPSConnection(SERVER_HOST, SERVER_PORT)
    payload = json.dumps({
        "group_id": group_id,
        "message": message
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/send_group_msg", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print("群消息发送结果:", data.decode("utf-8"))


# 主监听逻辑
def start_listener():
    print("启动加群请求监听器...")
    while True:
        try:
            # 获取群系统消息
            group_system_messages = get_group_system_messages()

            # 检查返回的 JSON 中是否有 join_requests
            if group_system_messages.get("status") == "ok" and group_system_messages.get("data"):
                join_requests = group_system_messages["data"].get("join_requests", [])
                for request in join_requests:
                    if not request.get("checked"):  # 仅处理未检查的请求
                        requester_uin = request["requester_uin"]  # 用户 QQ 号
                        group_id = request["group_id"]  # 申请加入的群号
                        flag = request["request_id"]  # 请求的唯一标识
                        apply_message = request.get("message", "")  # 加群请求附带的留言
                        print(f"处理加群请求: requester_uin={requester_uin}, group_id={group_id}, flag={flag}, message={apply_message}")
                        handle_group_request(requester_uin, group_id, flag, apply_message)
            else:
                print("未检测到有效的群系统消息或返回数据不正确。")

        except Exception as e:
            print("监听过程中发生错误:", str(e))

        # 轮询间隔
        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    start_listener()
