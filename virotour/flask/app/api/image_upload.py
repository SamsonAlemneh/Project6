import os

from flask import request, flash, redirect, jsonify

from app import allowed_file, app, db
from app.models import Tour, Location, Image


@app.route('/api/add/tour/images/<string:tour_name>', methods=['POST', 'GET'])
def api_add_tour_images(tour_name):
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        result = {}

        tour = db.session.query(Tour).filter(Tour.name == tour_name).first()
        location = Location(tour.id)
        db.session.add(location)
        db.session.commit()

        for file in files:
            if file and allowed_file(file.filename):
                filename_raw = file.filename
                filename = os.path.basename(filename_raw)
                target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'raw_images/')
                target_file = f'T_{tour.id}_L_{location.location_id}_{filename}'
                target_file_full = os.path.join(target_path, target_file)

                # To return to user
                result[filename] = f'raw_images/{target_file}'

                # Make directory & save
                os.makedirs(target_path, exist_ok=True)
                file.save(target_file_full)

                image = Image(location.location_id, result[filename])
                db.session.add(image)
                db.session.commit()

        flash('File(s) successfully uploaded')
        payload = {
            'tour_id': tour.id,
            'server_file_paths': result
        }
        return jsonify(payload), 200


@app.route('/api/tour/images/raw-images/<string:tour_name>/<int:location_id>', methods=['GET'])
def api_get_tour_images(tour_name, location_id):
    result = list()
    # Get Tour
    tour = db.session.query(Tour).filter(Tour.name == tour_name).first()
    # Get Location
    location = db.session.query(Location).filter((Location.tour_id == tour.id) &
                                                 (Location.location_id == location_id)).first()
    # Get Images
    images = db.session.query(Image).filter(Image.location_id == location.location_id).all()
    for image in images:
        result.append(image.file_path)

    payload = {
        'count': len(result),
        'server_file_paths': result
    }
    return jsonify(payload), 200


def api_set_panoramic_image(tour_name, location_id, path):
    """This is an internal call, so there is not a publically facing route."""
    # TODO
    return None


@app.route('/api/tour/images/panoramic-image/<string:tour_name>/<int:location_id>', methods=['POST', 'GET'])
def api_get_set_panoramic_image(tour_name, location_id):
    payload = {
        'server_file_path': 'TODO'
    }
    return jsonify(payload), 200
