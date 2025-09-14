from datetime import datetime, timedelta
import json

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def get_historical_data(days=7):
    """Get historical data for the specified number of days"""
    from backend.models import SensorData
    from backend.utils.database import db
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    data = SensorData.query.filter(
        SensorData.timestamp >= cutoff_date
    ).order_by(SensorData.timestamp.asc()).all()
    
    return data

def prepare_chart_data(sensor_data):
    """Prepare data for charts"""
    timestamps = [d.timestamp for d in sensor_data]
    moisture = [d.moisture for d in sensor_data]
    temperature = [d.temperature for d in sensor_data]
    humidity = [d.humidity for d in sensor_data]
    nitrogen = [d.nitrogen for d in sensor_data]
    phosphorus = [d.phosphorus for d in sensor_data]
    potassium = [d.potassium for d in sensor_data]
    
    return {
        'timestamps': timestamps,
        'moisture': moisture,
        'temperature': temperature,
        'humidity': humidity,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium
    }