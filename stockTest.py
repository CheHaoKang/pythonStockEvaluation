import urllib.request

print('Begin downloading stock info...')

url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20180720&type=ALL'
urllib.request.urlretrieve(url, 'stock_all_20180720.csv')


# import json
# with open('flask-stock-decken/potential_stocks.json', 'w', encoding='utf8') as outfile:
#     json.dump({'1337':['再生-KY', '不是', '是']}, outfile, ensure_ascii=False)
#
# with open('flask-stock-decken/potential_stocks.json', encoding='utf8') as f:
#     datastore = json.load(f)
#     print(datastore['1337'])
# import torch
# from torch.autograd import Variable
# from torch.optim import SGD
# import torch.nn as nn
#
# m1 = torch.ones(5, 3)
# m2 = torch.ones(5, 3)
#
# # 記得要將requires_grad設成True
# a = Variable(m1, requires_grad=True)
# b = Variable(m2, requires_grad=True)
#
# # 初始化優化器，使用SGD這個更新方式來更新a和b
# optimizer = SGD([a, b], lr=0.1)
#
# for _ in range(10):        # 我們示範更新10次
#     print(a+b)
#     print((a + b).sum())
#     loss = (a + b).sum()   # 假設a + b就是我們的loss
#
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()       # 更新
#
#     print(a)
#     print(b)
#
#     print('====================')
#
# m = nn.Linear(20, 30)
# input = torch.randn(128, 20, 30)
# print(input.size()[1:])
# # output = m(input)
# # print(input)
# # print(output.size())
# # print(output)
#
# target = torch.arange(1, 11)  # a dummy target, for example
# print(target)
# target = target.view(1, -1)
# print(target.size())