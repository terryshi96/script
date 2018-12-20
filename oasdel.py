# -*- encoding: utf-8 -*-
from oas.oas_api import OASAPI
from oas.ease.vault import Vault
import json
import datetime
from dateutil import rrule
# 阿里云oas定期删除归档

# 载入数据
def load(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


# 计算日期差
def days_between(start_date, end_date):
    days = rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date)
    return days.count()


def delete_file(vault_name, keep_num, keep_day):
    api = OASAPI('cn-hangzhou.oas.aliyuncs.com', 'xxxxx', 'xxxxx')
    vault = Vault.get_vault_by_name(api, vault_name)
    job = vault.retrieve_inventory()
    job.download_to_file(vault_name)
    data = load(vault_name)

    for item in data['ArchiveList']:
        # 归档日期
        date = datetime.datetime.strptime(item['CreationDate'], "%a, %d %b %Y %H:%M:%S %Z")
        # 当天日期
        today = datetime.date.today()
        # 删除超过keep_num天数的归档，跳过指定日期的归档, -1则不跳过
        if days_between(date, today) > keep_num and date.day != keep_day:
            # print item
            vault.delete_archive(item['ArchiveId'])
            # print date, days_between(date, today)
            # date - datetime.timedelta(days=90)


if __name__ == '__main__':
    vault_list = {
        'xxxx': {'keep_num': 30, 'keep_day': 30}
    }
    # delete_file('xxxxx',30,30)
    for item in vault_list.keys():
        delete_file(item, vault_list[item]['keep_num'], vault_list[item]['keep_day'])
