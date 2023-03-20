import os
import imagehash
from annoy import AnnoyIndex
from app.api.image_upload import api_get_tour_images
from PIL import Image


def compute_neighbors(tour_name, location_id):
    server_response = api_get_tour_images(tour_name, location_id)
    images_list = list(server_response['server_file_paths'])
    images_dir = "/path/to/images/on/server" # TODO: UPdates path to server. Tested with test path locally.

    # Create an integer id for each image, along with its corresponding vector of hash data.
    vector_length = 0
    id_to_vec = {}
    for count,f in enumerate(images_list):
        img = Image.open(''.join([images_dir,'/',f]))

        # Image hashes tell whether two images look nearly identical
        img_hash = imagehash.whash(img)
        hash_array = img_hash.hash.astype('int').flatten();
        vector_length = hash_array.shape[0]
        id_to_vec[count] = hash_array

    # Set up the AnnoyIndex and add this data to it.
    f = vector_length
    dist_function = "hamming"

    t = AnnoyIndex(f, dist_function)
    # iterate through the id_to_vec dictionary and added the keys and values to t
    for key,value in id_to_vec.items():
        t.add_item(key,value)

    # build ANNOY tree
    num_trees = 1
    t.build(num_trees)

    # Given an images in the images_list, find the nearest neighbors
    query_index = images_list.index(list(images_list)[0])
    num_neighbors = len(images_list)

    # Params to t.get_nns_by_item(...)
    # query_index: The index id of the query image.
    # num_neighbors: Number of nearest neighbors to return.
    # including_distances - setting this to true will return the distances of each of these neighbors to the query image.
    neighbors = t.get_nns_by_item(query_index,num_neighbors,include_distances=True) # Returns the n closest items

    img_hash = imagehash.whash(img)

    # imagehash convert the image to grayscale, so the color data is not preserved in the hash.
    img_hash = imagehash.colorhash(img)

    img_paths = [os.path.join(images_dir, images_list[i]) for i in neighbors[0]]

    returned_sequence = {
       'neighbors_distance': neighbors,
       'path': img_paths
    }

    return returned_sequence




