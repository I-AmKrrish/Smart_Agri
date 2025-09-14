from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from backend_files.config import Config

# Import routes
from routes.sensor_routes import sensor_bp
from routes.analytics_routes import analytics_bp
from routes.recommendation_routes import recommendation_bp

# Import data processor
from cloud_processing.data_processor import DataProcessor
from cloud_processing.crop_recommender import CropRecommender
from cloud_processing.fertilizer_recommender import FertilizerRecommender
from cloud_processing.analytics_engine import AnalyticsEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize components
    app.data_processor = DataProcessor()
    app.crop_recommender = CropRecommender('models/crop_recommender_model.pkl')
    app.fertilizer_recommender = FertilizerRecommender('models/fertilizer_recommender_model.pkl')
    
    # Register blueprints
    app.register_blueprint(sensor_bp)from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from backend_files.config import Config

# Import routes
from routes.sensor_routes import sensor_bp
from routes.analytics_routes import analytics_bp
from routes.recommendation_routes import recommendation_bp

# Import data processor
from cloud_processing.data_processor import DataProcessor
from cloud_processing.crop_recommender import CropRecommender
from cloud_processing.fertilizer_recommender import FertilizerRecommender
from cloud_processing.analytics_engine import AnalyticsEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize components
    app.data_processor = DataProcessor()
    app.crop_recommender = CropRecommender('models/crop_recommender_model.pkl')
    app.fertilizer_recommender = FertilizerRecommender('models/fertilizer_recommender_model.pkl')
    
    # Register blueprints
    app.register_blueprint(sensor_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(recommendation_bp)
    
    # Initialize with some historical data
    app.analytics_engine = AnalyticsEngine(app.data_processor.sensor_data)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Smart Agriculture API',
            'status': 'online',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(recommendation_bp)
    
    # Initialize with some historical data
    app.analytics_engine = AnalyticsEngine(app.data_processor.sensor_data)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Smart Agriculture API',
            'status': 'online',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)