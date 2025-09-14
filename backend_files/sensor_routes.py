from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from backend.models import SensorData, Alert
from backend.utils.database import db

sensor_bp = Blueprint('sensor', __name__, url_prefix='/api/sensor')

@sensor_bp.route('/data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['moisture', 'temperature', 'humidity', 'nitrogen', 'phosphorus', 'potassium']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Process the data
        processed_data = current_app.data_processor.process_incoming_data(data)
        
        # Store in database
        sensor_data = SensorData(
            device_id=data.get('device_id', 'unknown'),
            moisture=data['moisture'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium']
        )
        
        db.session.add(sensor_data)
        db.session.commit()
        
        # Generate alerts
        alerts = current_app.analytics_engine.generate_alerts(
            data, 
            current_app.data_processor.sensor_data.to_dict('list')
        )
        
        # Store alerts in database
        for alert in alerts:
            alert_record = Alert(
                type=alert['type'],
                message=alert['message'],
                severity=alert['severity']
            )
            db.session.add(alert_record)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Data received and processed successfully',
            'data': processed_data,
            'alerts': alerts
        }), 201
        
    except Exception as e:
        current_app.logger.error(f'Error processing sensor data: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@sensor_bp.route('/data', methods=['GET'])
def get_sensor_data():
    try:
        limit = request.args.get('limit', 100, type=int)
        device_id = request.args.get('device_id', None)
        
        query = SensorData.query
        
        if device_id:
            query = query.filter(SensorData.device_id == device_id)
        
        data = query.order_by(SensorData.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'data': [d.to_dict() for d in data],
            'count': len(data)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving sensor data: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@sensor_bp.route('/data/latest', methods=['GET'])
def get_latest_sensor_data():
    try:
        device_id = request.args.get('device_id', None)
        
        query = SensorData.query
        
        if device_id:
            query = query.filter(SensorData.device_id == device_id)
        
        data = query.order_by(SensorData.timestamp.desc()).first()
        
        if not data:
            return jsonify({'error': 'No data found'}), 404
        
        return jsonify(data.to_dict()), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving latest sensor data: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500