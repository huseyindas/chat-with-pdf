import re


def is_valid_uuid4(uuid_string):
    regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    return re.match(regex, uuid_string) is not None


def test_upload_pdf(test_client):
    files = {"file": ("test.pdf", open("./docs/huseyindascv.pdf", "rb"), "application/pdf")}
    response = test_client.post("/v1/pdf/", files=files)

    assert response.status_code == 200

    response_json = response.json()
    assert is_valid_uuid4(response_json["pdf_id"])

    files = {"file": ("test.pdf", open("./docs/image.png", "rb"), "application/image")}
    response = test_client.post("/v1/pdf/", files=files)

    assert response.status_code == 400


def test_chat(test_client):
    files = {"file": ("test.pdf", open("./docs/huseyindascv.pdf", "rb"), "application/pdf")}
    response = test_client.post(
        url="/v1/pdf/",
        files=files
    )

    assert response.status_code == 200

    response_json = response.json()
    pdf_id = response_json["pdf_id"]

    chat_response = test_client.post(
        url=f"/v1/chat/{pdf_id}",
        json={
            "message": "Who is the Huseyin Das?"
        }
    )

    assert chat_response.status_code == 200

    chat_response_json = chat_response.json()
    assert "response" in chat_response_json