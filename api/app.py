import json.decoder
import sys

import bson
from bson import json_util
from flask import Flask, jsonify, request, make_response, send_file
import io
from utils import scan_util
from utils import db_util
from flask_cors import CORS
from utils import report_util

app = Flask(__name__)
CORS(app, origins='*', methods=['GET', 'POST', 'DELETE'], allow_headers=['Content-Type'])


@app.route('/api/scan/execute', methods=['POST'])
def scan_execute():
    url = request.json['url']
    scan_name = request.json['scan_name']
    try:
        scan_details = scan_util.execute_full_scan(url)
    except json.decoder.JSONDecodeError as e:
        return jsonify({'error': 'Please initiate a scan again.'}), 500

    new_db_scan = db_util.create_scan(scan_name, url, scan_details)
    print(new_db_scan, file=sys.stderr)
    if new_db_scan is None:
        return jsonify({"error": "Unable to create new scan"}), 500
    scan_details_with_id = scan_details.copy()
    scan_details_with_id.update({"id": str(new_db_scan)})
    return jsonify(scan_details_with_id)


@app.route('/api/scan/all', methods=['GET'])
def get_all_scans():
    scans = db_util.get_all_scans()
    return jsonify(scans)


@app.route('/api/scan/<scan_id>/get', methods=['GET'])
def get_scan(scan_id):
    try:
        scan = db_util.get_scan_details(scan_id)
    except bson.errors.InvalidId:
        return jsonify({"error": "Invalid ID"}), 404
    if scan is None:
        return jsonify({"error": "Scan not found"}), 404

    print(scan['scan_name'], file=sys.stderr)
    return jsonify(scan)


@app.route('/api/scan/<scan_id>/delete', methods=['DELETE'])
def delete_scan(scan_id):
    scan = db_util.delete_scan(scan_id)
    if scan is None:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({"msg": "Scan deleted"}), 200


@app.route('/api/scan/<scan_id>/download', methods=['GET'])
def download_report(scan_id):
    try:
        scan = db_util.get_scan_details(scan_id)
    except bson.errors.InvalidId:
        return jsonify({"error": "Invalid ID"}), 404

    if scan is None:
        return jsonify({"error": "Scan not found"}), 404

    pdf_stream = io.BytesIO(report_util.generate_report_from_json(scan, str(scan["_id"]["$oid"])))

    return send_file(pdf_stream, download_name=f'{str(scan["_id"]["$oid"])}.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run()
