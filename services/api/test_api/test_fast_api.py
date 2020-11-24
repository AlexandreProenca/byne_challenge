from flask import url_for

signed_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWNyb3NlcnZpY2VfaWQiOiIxMjM0NTY3ODkwIn0.l9u4wnxv7h0o8JwMgVCZ6p_bC19bBf5xQYIg3SsKCC0'


def test_app(client):
    assert client.get(url_for('get_number', token=signed_token)).status_code == 200
