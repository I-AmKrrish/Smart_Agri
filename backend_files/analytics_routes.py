from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from backend.models import SensorData, Alert
from backend.utils.database import db
from backend.utils.helpers import get_historical_data, prepare_chart_data

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/current', methods=['GET'])
def get_current_data():
    try:
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            return jsonify({'error': 'No data available'}), 404
        
        # Get historical data for charts (last 7 days)
        historical_data = get_historical_data(7)
        chart_data = prepare_chart_data(historical_data)
        
        # Calculate health score
        current_conditions = {
            'moisture': latest_data.moisture,
            'temperature': latest_data.temperature,
            'nitrogen': latest_data.nitrogen,
            'phosphorus': latest_data.phosphorus,
            'potassium': latest_data.potassium
        }
        
        health_score = current_app.analytics_engine.assess_crop_health(current_conditions)
        
        # Get active alerts
        active_alerts = Alert.query.filter_by(resolved=False).all()
        
        return jsonify({
            'current': latest_data.to_dict(),
            'historical': chart_data,
            'healthScore': health_score,
            'alerts': [alert.to_dict() for alert in active_alerts]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving current data: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@analytics_bp.route('/health', methods=['GET'])
def get_health_score():
    try:
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            return jsonify({'error': 'No data available'}), 404
        
        # Calculate health score
        current_conditions = {
            'moisture': latest_data.moisture,
            'temperature': latest_data.temperature,
            'nitrogen': latest_data.nitrogen,
            'phosphorus': latest_data.phosphorus,
            'potassium': latest_data.potassium
        }
        
        health_score = current_app.analytics_engine.assess_crop_health(current_conditions)
        
        return jsonify({
            'healthScore': health_score,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error calculating health score: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@analytics_bp.route('/yield-prediction', methods=['GET'])
def get_yield_prediction():
    try:
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            return jsonify({'error': 'No data available'}), 404
        
        # Get crop type from query parameter or use default
        crop_type = request.args.get('crop', 'Wheat')
        
        # Prepare current conditions
        current_conditions = {
            'moisture': latest_data.moisture,
            'temperature': latest_data.temperature,
            'nitrogen': latest_data.nitrogen,
            'phosphorus': latest_data.phosphorus,
            'potassium': latest_data.potassium
        }
        
        # Get historical data for moisture
        historical_data = get_historical_data(7)
        moisture_data = [d.moisture for d in historical_data]
        
        # Predict yield
        predicted_yield = current_app.analytics_engine.predict_yield(
            current_conditions, 
            crop_type
        )
        
        # Check for water stress
        water_stress = current_app.analytics_engine.detect_water_stress(moisture_data)
        
        return jsonify({
            'predictedYield': predicted_yield,
            'crop': crop_type,
            'waterStress': water_stress,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error predicting yield: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@analytics_bp.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        resolved = request.args.get('resolved', 'false').lower() == 'true'
        limit = request.args.get('limit', 50, type=int)
        
        alerts = Alert.query.filter_by(resolved=resolved).order_by(
            Alert.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'alerts': [alert.to_dict() for alert in alerts],
            'count': len(alerts)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving alerts: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@analytics_bp.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.resolved = True
        db.session.commit()
        
        return jsonify({
            'message': 'Alert resolved successfully',
            'alert': alert.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error resolving alert: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500