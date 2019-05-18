def test_icu(client):
    res = client.get('/996')
    data = {'江苏润恒物流发展有限公司（集团）', '德邦物流', '上海鱼泡泡信息科技有限公司', '美的集团', '小红书', '京东', '百度', '阿里巴巴', '蚂蚁金服', '小米', '华为'}
    assert len(list(filter(lambda item: item.get('company') in data, res.json))) == len(data)
