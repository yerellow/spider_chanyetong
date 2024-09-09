import requests
import pandas as pd
proxy_ip = "https://127.0.0.1:8888"
# 设置代理信息
proxies = {"http": proxy_ip}
key = 'lmpWmKOQskvkDg3vokx9WG1DvPgD4AEDdW8qFu0If9'
# 发起请求
url = 'https://www.chanyeos.com/industry_knowledge_engine/v2/industryChannel/industry_link?industry_code=INB1219&area_key=310000&special_tag='
d ={
    'industry_code': 'INB1219',
    'second_special_tag': '',
    'area_key': '310000',
}


head = {
    'cookie': '_xsrf=2|ca762977|50a12c4ded5fb03689f322d777d943b0|1703662474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'referer': 'https://www.chanyeos.com/smart-ke/',
    'Authorization': f'Bearer {key}'
}
resp = requests.get(url, headers=head, data=d, proxies=proxies)
code = resp.json().get('data')
ch1 = code.get('children')
def extract_titles_and_values(data):
    titles_and_values = []
    for child in data['children']:
        titles_and_values.append({'title': child['title'], 'value': child['value']})
        print(child['title'], child['value'])
    return titles_and_values


def get_data(value, key):
    proxy_ip = "https://127.0.0.1:8888"
    # 设置代理信息
    proxies = {"http": proxy_ip}

    url = 'https://www.chanyeos.com/industry_knowledge_engine/v2/industryChannel/industry_link_company_list'
    d = {
        'industry_code': 'INB1219',
        'second_special_tag': '',
        'link_code': value,
        'area_key': '310000',
        'page_size': '20',
    }

    head = {
        'cookie': '_xsrf=2|ca762977|50a12c4ded5fb03689f322d777d943b0|1703662474',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'referer': 'https://www.chanyeos.com/smart-ke/',
        'Authorization': f'Bearer {key}'
    }

    # 创建一个列表，保存所有结果
    all_results = []

    # 循环获取数据，直到返回空列表
    page_number = 1
    while True:
        d['page_number'] = str(page_number)
        resp = requests.post(url, headers=head, json=d, proxies=proxies)
        response_data = resp.json()
        table_body_data = response_data['data']['tableBody']

        # 如果返回的 'tableBody' 为空列表，则停止循环
        if not table_body_data:
            break

        # 提取 'tableBody' 中的值
        result_list = []

        # 遍历 'tableBody' 中的字典，提取值
        for entry in table_body_data:
            result_list.append({
                'id': entry.get('id'),
                'name': entry.get('name'),
                'special_tag': entry.get('special_tag'),
                'in_area': entry.get('in_area'),
                'index': entry.get('index')
            })

        # 将当前页的结果添加到总结果列表
        all_results.extend(result_list)

        # 增加页数
        page_number += 1
    return all_results


# 将你提供的字典作为参数传递给函数
dat = code  # 省略了部分数据

'''result = extract_titles_and_values(dat)'''
'''[{'title': '原材料加工制造', 'value': 'INB121906'}, {'title': '新能源汽车零部件', 'value': 'INB121907'}, {'title': '新能源汽车整车制造', 'value': 'INB121908'}, {'title': '新能源汽车相关服务（充电及后市场服务)', 'value': 'INB121909'}, {'title': '新能源汽车相关设施制造', 'value': 'INB121910'}]'''
result = [{'title': '原材料加工制造', 'value': 'INB121906'}, {'title': '新能源汽车零部件', 'value': 'INB121907'}]
dict = {}
for item in result:
    dict[item['title']] = get_data(item['value'], key)
    print(item['title'])
    print(dict)
data = dict
print(data)
df = pd.DataFrame(columns=['Key', 'id', 'name', 'special_tag', 'in_area', 'index'])

# Iterate through the dictionary and append rows to the DataFrame
for key, value in data.items():
    for entry in value:
        df = df._append({'Key': key, 'id': entry.get('id'), 'name': entry.get('name'), 'special_tag': entry.get('special_tag'), 'in_area': entry.get('in_area'), 'index': entry.get('index')}, ignore_index=True)

# Save the DataFrame to an Excel file
df.to_excel('x2.xlsx', index=False)