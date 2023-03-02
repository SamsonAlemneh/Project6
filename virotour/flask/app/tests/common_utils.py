import json
import os


def list_tours(client):
    return parse_http_response(client.get('/api/tours'))


def get_tour_by_id(client, id):
    return parse_http_response(client.get(f'/api/tour/{id}'))


def get_tour_by_name(client, name):
    return parse_http_response(get_tour_by_name_with_resp(client, name))


def get_tour_by_name_with_resp(client, name):
    return client.get(f'/api/tour-name/{name}')


def add_tour(client, name, description):
    return parse_http_response(
        client.post('/api/add/tour', json={
            'name': name,
            'description': description
        })
    )


def update_tour(client, name, description):
    return parse_http_response(update_tour_with_resp(client, name, description))


def update_tour_with_resp(client, name, description):
    resp = get_tour_by_name_with_resp(client, name)
    if resp.status_code != 200:
        return resp

    tour = parse_http_response(resp)
    id = tour['id']
    resp = client.post(f'/api/update/tour/{id}', json={
        'name': name,
        'description': description
    })

    return resp


def delete_tour(client, name, description):
    return parse_http_response(delete_tour_with_resp(client, name, description))


def delete_tour_with_resp(client, name, description):
    resp = get_tour_by_name_with_resp(client, name)
    if resp.status_code != 200:
        return resp

    tour = parse_http_response(resp)
    id = tour['id']
    resp = client.post(f'/api/delete/tour/{id}', json={
        'name': name,
        'description': description
    })

    return resp


def upload_images(client, name, image_list):
    return parse_http_response(upload_images_with_resp(client, name, image_list))


def upload_images_with_resp(client, name, image_list):
    files = []
    try:
        files = [open(fpath, 'rb') for fpath in image_list]
        return client.post(f'/api/add/tour/images/{name}', data={
            'files[]': files
        })
    finally:
        for fp in files:
            fp.close()


def get_image_paths(path):
    image_dir = os.path.join(os.path.dirname(__file__), 'images', path)
    image_list = os.listdir(image_dir)
    return [f"{image_dir}/{file}" for file in image_list]
    pass


def get_raw_images(client, tour_name, location_id):
    return parse_http_response(get_raw_images_with_resp(client, tour_name, location_id))


def get_raw_images_with_resp(client, tour_name, location_id):
    return client.get(f'/api/tour/images/raw-images/{tour_name}/{location_id}')


def compute_tour(client, name):
    return parse_http_response(compute_tour_with_resp(client, name))


def compute_tour_with_resp(client, name):
    return client.get(f'/api/compute-tour/{name}')


def get_panoramic_image(client, tour_name, location_id):
    return parse_http_response(get_panoramic_image_with_resp(client, tour_name, location_id))


def get_panoramic_image_with_resp(client, tour_name, location_id):
    return client.get(f'/api/tour/images/panoramic-image/{tour_name}/{location_id}')


def set_panoramic_image(client, tour_name, location_id, path):
    return parse_http_response(get_raw_images_with_resp(client, tour_name, location_id, path))


def set_panoramic_image_with_resp(client, tour_name, location_id, path):
    return client.post(f'/api/tour/images/panoramic-image/{tour_name}/{location_id}', data={
        'panoramic_path': path
    })


def parse_http_response(resp):
    try:
        print(str(resp))
        return json.loads(resp.data.decode())
    except:
        raise Exception(resp.data)
