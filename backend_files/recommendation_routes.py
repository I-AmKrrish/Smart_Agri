from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from backend.models import Recommendation, SensorData
from backend.utils.database import db

recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/api/recommendations')

@recommendation_bp.route('/crops', methods=['GET'])
def get_crop_recommendations():
    try:
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            return jsonify({'error': 'No data available'}), 404
        
        # Prepare features for ML model
        features = [[
            latest_data.moisture,
            latest_data.temperature,
            latest_data.humidity,
            latest_data.nitrogen,
            latest_data.phosphorus,
            latest_data.potassium
        ]]
        
        # Get crop recommendations
        recommendations = current_app.crop_recommender.recommend_crop(features)
        
        # Store recommendation in database
        recommendation = Recommendation(
            recommendation_type='crop',
            data={
                'recommendations': recommendations,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        return jsonify({
            'recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error generating crop recommendations: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@recommendation_bp.route('/fertilizer', methods=['GET'])
def get_fertilizer_recommendations():
    try:
        # Get latest sensor data
        latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest_data:
            return jsonify({'error': 'No data available'}), 404
        
        # Get crop type from query parameter or use default
        crop_type = request.args.get('crop', 'Wheat')
        
        # Prepare features for ML model
        features = [[
            latest_data.moisture,
            latest_data.temperature,
            latest_data.humidity,
            latest_data.nitrogen,
            latest_data.phosphorus,
            latest_data.potassium
        ]]
        
        # Get fertilizer recommendations
        recommendation = current_app.fertilizer_recommender.recommend_fertilizer(
            features, crop_type
        )
        
        # Store recommendation in database
        recommendation_record = Recommendation(
            recommendation_type='fertilizer',
            data={
                'recommendation': recommendation,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        db.session.add(recommendation_record)
        db.session.commit()
        
        return jsonify({
            'recommendation': recommendation,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error generating fertilizer recommendations: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@recommendation_bp.route('/history', methods=['GET'])
def get_recommendation_history():
    try:
        limit = request.args.get('limit', 10, type=int)
        rec_type = request.args.get('type', None)
        
        query = Recommendation.query
        
        if rec_type:
            query = query.filter(Recommendation.recommendation_type == rec_type)
        
        recommendations = query.order_by(
            Recommendation.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'recommendations': [rec.to_dict() for rec in recommendations],
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving recommendation history: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500