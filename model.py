import base64

import requests


def converter(arr_topics, url):
    im_url = url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response_ = requests.get(im_url, headers=headers)
    image_data = response_.content

    def encode_image(image_data):
        return base64.b64encode(image_data).decode("utf-8")

    image_b64 = encode_image(image_data)

    tags = arr_topics

    url = "http://10.0.11.2:30068/api/generate"

    data = {
        "model": "gemma3:12b",
        "prompt": f"""
    You are ranking this image from these tags and your own tags.

    first take these tags:
    {tags}
    Check the image and add any tags you think are relevant to the image. Then add your own tags up to the best 10 from your own after these tags.
    Then rank all the tags by importance to the image and assign a weight between 0 and 1 to each tag.
    Higher weight means more important visually.
    Keep only the most important tags
    Assign a weight between 0 and 1

    Format:
    [
    {{"tag":"dog","weight":0.95}},
    {{"tag":"out","weight":0.80}}
    ]

    - Make sure to only ever respond with JSON only. No other text is allowed.
    """,
        "images": [image_b64],
        "stream": False,
    }

    response = requests.post(url, json=data)
    return response.json()["response"]


# im_url="https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_November_2010-1a.jpg"
# tags = [
#     "cat", "orange", "sofa", "indoor",
#     "pet", "living room", "relaxed", "animal"
# ]
# converter(tags,im_url)
