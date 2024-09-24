import requests
import time
from pymongo import MongoClient

# 递归提取 JSON 数据中的 title 和 value 对
# def extract_titles_and_values(data):
#     def recursive_extract(children):
#         titles_and_values = []  # 用于存储 title 和 value 的列表
#         for child in children:  # 遍历每个节点
#             if child.get('children'):  # 如果有子节点，则递归处理
#                 titles_and_values.extend(recursive_extract(child['children']))
#             else:  # 如果没有子节点，提取 title 和 value
#                 titles_and_values.append({'title': child['title'], 'value': child['value']})
#                 print({'title': child['title'], 'value': child['value']})  # 打印出 title 和 value
#         return titles_and_values
#     result = recursive_extract(data['children'])  # 从 JSON 的 'children' 开始递归
#     return result

def extract_titles_and_values(data):
    result = [
        # {'title': '原材料加工制造', 'value': 'INB121906'},
        # {'title': '电池', 'value': 'INB1219070101'},
        # {'title': '电机系统', 'value': 'INB1219070102'},
        # {'title': '电控系统', 'value': 'INB1219070103'},
        # {'title': '新能源汽车基础零部件', 'value': 'INB12190702'},
        # {'title': '感知系统', 'value': 'INB1219070301'},
        # {'title': '执行与控制系统', 'value': 'INB1219070302'},
        # {'title': '决策系统', 'value': 'INB1219070303'},
        # {'title': '车联网与信息交互', 'value': 'INB1219070304'},
        # {'title': '智能座舱系统', 'value': 'INB1219070305'},
        # {'title': '其他智能车载设备', 'value': 'INB1219070306'},
        {'title': '新能源汽车整车制造', 'value': 'INB121908'},]
        # {'title': '纯电动汽车', 'value': 'INB12190801'},
        # {'title': '燃料电池汽车', 'value': 'INB12190802'},
        # {'title': '插电式混动动力车', 'value': 'INB12190803'},
        # {'title': '增程式混动动力车', 'value': 'INB12190804'},
        # {'title': '新能源汽车相关服务', 'value': 'INB121909'},
        # {'title': '新能源汽车相关设施制造', 'value': 'INB121910'}]
    return result
# 获取 API 数据并存储到 MongoDB 中
def get_data(title, value, key, proxies, db, collection):
    url = 'https://www.chanyeos.com/industry_knowledge_engine/v2/industryChannel/industry_link_company_list'
    d = {
        'industry_code': 'INB1219',  # 行业代码
        'second_special_tag': '',
        'link_code': value,  # 传入的 value 作为 link_code
        'area_key': '310000',  # 区域代码
        'page_size': '20',  # 每页获取 20 条数据
    }

    head = {
        'cookie': '_xsrf=2|ca762977|50a12c4ded5fb03689f322d777d943b0|1703662474',  # Cookie 信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',  # 用户代理信息
        'referer': 'https://www.chanyeos.com/smart-ke/',  # 引用页面
        'Authorization': f'Bearer {key}'  # Bearer 令牌
    }

    page_number = 1  # 初始页码
    while True:  # 分页循环
        d['page_number'] = str(page_number)  # 更新页码
        resp = requests.post(url, headers=head, json=d, proxies=proxies)  # POST 请求获取数据
        response_data = resp.json()  # 将响应转换为 JSON
        table_body_data = response_data['data'].get('tableBody', [])  # 获取表格中的数据

        if not table_body_data:  # 如果没有数据，则退出循环
            break

        for entry in table_body_data:  # 遍历每条数据
            save_to_mongodb({'Key': title, **entry}, db, collection)  # 保存到 MongoDB

        print(f"{title}爬完了第{page_number}页")
        page_number += 1  # 增加页码

        if page_number % 5 == 0:  # 每爬 5 页暂停 1 秒
            print(f"{title}暂停1秒...")
            time.sleep(1)

# 将数据保存到 MongoDB
def save_to_mongodb(data, db, collection):
    client = MongoClient('mongodb://localhost:27017/')  # 连接 MongoDB
    db = client[db]  # 选择数据库
    collection = db[collection]  # 选择集合
    try:
        collection.delete_many({'id': data['id'], 'Key': data['Key']})  # 删除已有的相同 id 数据
        collection.insert_one(data)  # 插入新数据
        print(f'数据插入成功: {data["name"]}')
    except Exception as e:  # 异常处理
        print(f'数据插入失败: {e}')

# 获取行业的代码信息
def fetch_data(key, proxies):
    url = 'https://www.chanyeos.com/industry_knowledge_engine/v2/industryChannel/industry_link?industry_code=INB1219&area_key=310000&special_tag='
    d = {
        'industry_code': 'INB1219',  # 行业代码
        'second_special_tag': '',
        'area_key': '310000',  # 区域代码
    }

    head = {
        'cookie': '_xsrf=2|ca762977|50a12c4ded5fb03689f322d777d943b0|1703662474',  # Cookie 信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',  # 用户代理信息
        'referer': 'https://www.chanyeos.com/smart-ke/',  # 引用页面
        'Authorization': f'Bearer {key}'  # Bearer 令牌
    }

    resp = requests.get(url, headers=head, data=d, proxies=proxies)  # GET 请求获取行业代码数据
    code = resp.json().get('data')  # 返回数据
    return code

# 主函数，执行数据抓取流程
def main():
    proxy_ip = "https://127.0.0.1:8888"  # 代理地址
    proxies = {"http": proxy_ip}  # 代理设置
    key = 'Yd4EUp0eUzeB9XQsYVYDvuQxl6aQ7bBt9GMQsGT59w'  # Bearer 令牌

    data = fetch_data(key, proxies)  # 获取行业代码数据
    result = extract_titles_and_values(data)  # 提取标题和对应的值

    db_name = 'chanyet'  # MongoDB 数据库名
    collection_name = 'comp2'  # MongoDB 集合名
    i = 1  # 计数器
    for item in result:
        if i < 1:
            print(i)
            i += 1
        else:
            print(i)
            i += 1
            title = item['title']  # 获取 title
            value = item['value']  # 获取 value
            print(f"正在获取{title}的数据...")
            get_data(title, value, key, proxies, db_name, collection_name)  # 获取并保存数据

# 程序入口
if __name__ == "__main__":
    main()
