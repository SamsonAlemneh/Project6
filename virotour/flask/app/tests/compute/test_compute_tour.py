import os

from PIL import Image
from app import app
from app.tests.common_utils import add_tour, get_image_paths, upload_images, compute_tour, get_panoramic_image, \
    get_raw_images


def test_compute_tour(client):
    tour_name = "tour-1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    compute_tour(client, tour_name)

    # Test get relative image path
    pano_image_path = get_panoramic_image(client, tour_name, 1)['server_file_path']
    assert pano_image_path == 'panoramic_images/T_1_L_1_pano.png'

    # Test image exists and is openable
    pano_image_path = os.path.join(app.config['UPLOAD_FOLDER'], pano_image_path)
    img = Image.open(pano_image_path)
    # img.show()

    # Test that we can still retrieve the original images if needed
    data = get_raw_images(client, "tour-1", 1)
    assert data['count'] == 5
    assert data['server_file_paths'][0] == 'raw_images/T_1_L_1_S1.jpg'
