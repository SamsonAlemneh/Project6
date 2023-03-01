from app.api.compute.image_extract_text import image_extract_text
from app.tests.common_utils import add_tour, get_image_paths, upload_images


def test_image_extract_text(client):
    tour_name = "Tour 1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    data = image_extract_text(tour_name, 1)

    assert True == False