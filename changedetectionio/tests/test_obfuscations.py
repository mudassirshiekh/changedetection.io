#!/usr/bin/python3

import time
from flask import url_for
from .util import live_server_setup, wait_for_all_checks


def set_original_ignore_response():
    test_return_data = """<html>
       <body>
     <span>The price is</span><span>$<!-- -->90<!-- -->.<!-- -->74</span>
     </body>
     </html>

    """

    with open("test-datastore/endpoint-content.txt", "w") as f:
        f.write(test_return_data)


def test_obfuscations(client, live_server):
    set_original_ignore_response()
    live_server_setup(live_server)

    # Add our URL to the import page
    test_url = url_for('test_endpoint', _external=True)
    res = client.post(
        url_for("import_page"),
        data={"urls": test_url},
        follow_redirects=True
    )
    assert b"1 Imported" in res.data

    # Give the thread time to pick it up
    wait_for_all_checks(client)

    # Check HTML conversion detected and workd
    res = client.get(
        url_for("preview_page", uuid="first"),
        follow_redirects=True
    )
    # whitespace appears but it renders https://github.com/weblyzard/inscriptis/issues/45#issuecomment-1923339265
    assert b'$ 90.74' in res.data
