from app.api.compute.pano_util import stitch
from app.api.image_upload import api_get_tour_images
from setuptools.namespaces import flatten


def compute_panoramic(tour_name, location_id):
    image_list = api_get_tour_images(tour_name, location_id)
    file_paths = [x for x in image_list[0].json['server_file_paths']]
    args = ["--img_names", file_paths,
            "--warp", "spherical",
            "--features", "orb",
            "--matcher", "homography",
            "--estimator", "homography",
            "--match_conf", "0.3",
            "--conf_thresh", "0.3",
            "--ba", "ray",
            "--ba_refine_mask", "xxxxx",
            "--wave_correct", "horiz",
            "--warp", "compressedPlaneA2B1",
            "--blend", "multiband",
            "--expos_comp", "channel_blocks",
            "--seam", "gc_colorgrad"]
    flatlist = []
    for element in args:
        if type(element) == str:
            flatlist.append(element)
        else:
            for inner_element in element:
                flatlist.append(inner_element)
    stitch.main(flatlist)
    pass
