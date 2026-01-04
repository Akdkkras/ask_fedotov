from urllib.parse import parse_qs


def application(environ, start_response):
    get_params = parse_qs(environ.get("QUERY_STRING", ""))

    post_params = {}
    if environ.get("REQUEST_METHOD") == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            content_length = 0

        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        post_params = parse_qs(body)

    response_body = [
        "GET parameters:\n",
        str(get_params),
        "\n\nPOST parameters:\n",
        str(post_params),
    ]

    response = "".join(response_body).encode("utf-8")

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(response))),
        ],
    )
    return [response]
