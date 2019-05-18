def test_404_data(client):
    res = client.get('/idontthinkthispagewillexist')
    assert '404-SUMSC' in res.data.decode('utf-8')


def test_404_code(client):
    res = client.get('/idontthinkthispagewillexist')
    assert res.status_code == 404


def test_404_file(app):
    import os
    assert os.path.exists(os.path.join(app.root_path, 'templates/404.html'))
