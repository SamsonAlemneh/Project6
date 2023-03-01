from app.api.compute.pano_util import stitch
from app.api.image_upload import api_get_tour_images
from setuptools.namespaces import flatten


def compute_panoramic(tour_name, location_id):
    image_list = api_get_tour_images(tour_name, location_id)
    file_paths = [x for x in image_list[0].json['server_file_paths']]
    args = ["--img_names", file_paths]
    flatlist = []
    for element in args:
        if type(element) == str:
            flatlist.append(element)
        else:
            for inner_element in element:
                flatlist.append(inner_element)
    stitch.main(flatlist)
    pass
