from app.api.compute.image_extract_text import image_extract_text, compute_extracted_text_list
from app.tests.common_utils import add_tour, get_image_paths, upload_images

def test_extract_text_from_image_with_text(client):
    tour_name = "Tour 1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    # data = image_extract_text(tour_name, 1)

    data = compute_extracted_text_list('../images/input_images/location1/museum.jpg')

    assert len(data) == 15      # easyocr found 15 extracted text objects in this specific image (hard coded in image_extract_text; still
                                # awaiting computed panoramic image)

    for currentText in data:
        print(currentText)
        assert len(currentText['position']) == 3    
        assert currentText['position']['x'] != None
        assert currentText['position']['y'] != None
        assert currentText['content'] != ""

def test_extract_text_from_image_with_no_text(client):
    tour_name = "Tour 1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    data = compute_extracted_text_list('../images/input_images/location1/S2.jpg')

    assert len(data) == 0
