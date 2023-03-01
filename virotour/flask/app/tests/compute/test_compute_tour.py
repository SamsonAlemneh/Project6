from PIL import Image
from app.tests.common_utils import add_tour, get_image_paths, upload_images, compute_tour, get_panoramic_image


def test_compute_tour(client):
    tour_name = "tour-1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    compute_tour(client, tour_name)

    pano_image_path = get_panoramic_image(client, tour_name, 1)
    # pano_image_path = r"C:\Users\Ivo\Documents\spring2023\virotour\flask\uploads\panoramic_images\T_1_L_1_pano.png"

    img = Image.open(pano_image_path)
    # img.show()