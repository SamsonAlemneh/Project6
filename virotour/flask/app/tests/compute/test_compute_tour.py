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

    pano_image_path = get_panoramic_image(client, tour_name, 1)['server_file_path']
    pano_image_path = os.path.join(app.config['UPLOAD_FOLDER'], pano_image_path)
    # pano_image_path = r"C:\Users\Ivo\Documents\spring2023\virotour\flask\uploads\panoramic_images\T_1_L_1_pano.png"

    img = Image.open(pano_image_path)
    # img.show()

    # Validates that we can still retrieve the original images
    data = get_raw_images(client, "Tour 1", 1)
    assert data['count'] == 5
    assert data['server_file_paths'] == [
        'raw_images/T_1_L_1_S1.jpg',
        'raw_images/T_1_L_1_S2.jpg',
        'raw_images/T_1_L_1_S3.jpg',
        'raw_images/T_1_L_1_S4.jpg',
        'raw_images/T_1_L_1_S5.jpg'
    ]