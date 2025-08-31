"""
Advanced Celery Tasks for AI/ML Processing in Farmazee Enterprise Platform.

This module contains background tasks for machine learning operations,
computer vision analysis, and intelligent recommendations.
"""

import logging
import time
from celery import shared_task, current_task
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import numpy as np
import pandas as pd
from PIL import Image
import io
import base64

from .models import (
    AIModel, Prediction, ComputerVisionAnalysis, 
    Recommendation, TrainingJob, DataSource
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='ai_ml.tasks.train_model')
def train_model(self, model_id, training_config=None):
    """
    Train an AI/ML model with the given configuration.
    
    Args:
        model_id: UUID of the AIModel to train
        training_config: Optional training configuration override
    """
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 100, 'status': 'Initializing training...'}
        )
        
        # Get the model
        model = AIModel.objects.get(id=model_id)
        
        # Create or get training job
        training_job, created = TrainingJob.objects.get_or_create(
            model=model,
            defaults={
                'status': 'running',
                'training_config': training_config or {},
                'total_epochs': training_config.get('epochs', 100) if training_config else 100,
                'started_at': timezone.now()
            }
        )
        
        if not created:
            training_job.status = 'running'
            training_job.started_at = timezone.now()
            training_job.save()
        
        # Simulate training process
        total_epochs = training_job.total_epochs
        
        for epoch in range(total_epochs):
            # Update progress
            progress = (epoch + 1) / total_epochs * 100
            current_task.update_state(
                state='PROGRESS',
                meta={
                    'current': epoch + 1,
                    'total': total_epochs,
                    'status': f'Training epoch {epoch + 1}/{total_epochs}'
                }
            )
            
            # Simulate training time
            time.sleep(0.1)
            
            # Update training job
            training_job.progress_percentage = progress
            training_job.current_epoch = epoch + 1
            training_job.training_loss = 1.0 - (epoch / total_epochs) * 0.8
            training_job.validation_loss = 1.0 - (epoch / total_epochs) * 0.7
            training_job.training_accuracy = (epoch / total_epochs) * 0.9
            training_job.validation_accuracy = (epoch / total_epochs) * 0.85
            training_job.save()
        
        # Complete training
        training_job.status = 'completed'
        training_job.completed_at = timezone.now()
        training_job.duration = training_job.completed_at - training_job.started_at
        training_job.progress_percentage = 100.0
        training_job.save()
        
        # Update model metrics
        model.accuracy = training_job.validation_accuracy
        model.precision = training_job.validation_accuracy * 0.95
        model.recall = training_job.validation_accuracy * 0.92
        model.f1_score = 2 * (model.precision * model.recall) / (model.precision + model.recall)
        model.status = 'active'
        model.last_trained = timezone.now()
        model.training_duration = training_job.duration
        model.save()
        
        logger.info(f"Model {model.name} training completed successfully")
        
        return {
            'status': 'Training completed successfully',
            'model_id': str(model_id),
            'accuracy': model.accuracy,
            'duration': str(training_job.duration)
        }
        
    except Exception as exc:
        logger.error(f"Error training model {model_id}: {exc}")
        
        # Update training job status
        if 'training_job' in locals():
            training_job.status = 'failed'
            training_job.error_message = str(exc)
            training_job.save()
        
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task(bind=True, name='ai_ml.tasks.make_prediction')
def make_prediction(self, model_id, user_id, input_data, prediction_type):
    """
    Make a prediction using the specified AI model.
    
    Args:
        model_id: UUID of the AIModel to use
        user_id: ID of the user making the prediction
        input_data: Input data for prediction
        prediction_type: Type of prediction to make
    """
    try:
        # Get the model and user
        model = AIModel.objects.get(id=model_id, status='active')
        user = User.objects.get(id=user_id)
        
        # Simulate prediction processing
        time.sleep(0.5)
        
        # Generate mock prediction result based on type
        if prediction_type == 'crop_yield':
            result = {
                'predicted_yield': round(np.random.uniform(2.5, 4.5), 2),
                'confidence_interval': [round(np.random.uniform(2.0, 5.0), 2), round(np.random.uniform(2.5, 5.5), 2)],
                'factors': ['soil_quality', 'weather_conditions', 'fertilizer_application'],
                'recommendations': ['Increase irrigation', 'Apply nitrogen fertilizer', 'Monitor for pests']
            }
        elif prediction_type == 'disease_risk':
            result = {
                'risk_level': np.random.choice(['low', 'medium', 'high']),
                'risk_score': round(np.random.uniform(0.1, 0.9), 2),
                'symptoms': ['yellowing_leaves', 'stunted_growth', 'leaf_spots'],
                'prevention_measures': ['Improve air circulation', 'Apply fungicide', 'Remove infected plants']
            }
        elif prediction_type == 'market_price':
            result = {
                'predicted_price': round(np.random.uniform(25, 75), 2),
                'price_trend': np.random.choice(['increasing', 'decreasing', 'stable']),
                'market_factors': ['demand_supply', 'weather_conditions', 'export_demand'],
                'timing_recommendation': np.random.choice(['sell_now', 'hold', 'wait_for_better_price'])
            }
        else:
            result = {
                'prediction': 'Sample prediction result',
                'confidence': round(np.random.uniform(0.6, 0.95), 2)
            }
        
        # Calculate confidence score
        confidence_score = round(np.random.uniform(0.7, 0.95), 2)
        
        # Determine confidence level
        if confidence_score < 0.6:
            confidence_level = 'low'
        elif confidence_score < 0.8:
            confidence_level = 'medium'
        elif confidence_score < 0.95:
            confidence_level = 'high'
        else:
            confidence_level = 'very_high'
        
        # Create prediction record
        prediction = Prediction.objects.create(
            model=model,
            user=user,
            prediction_type=prediction_type,
            input_data=input_data,
            prediction_result=result,
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            expires_at=timezone.now() + timedelta(days=30)
        )
        
        logger.info(f"Prediction created successfully: {prediction.id}")
        
        return {
            'prediction_id': str(prediction.id),
            'confidence_score': confidence_score,
            'result': result
        }
        
    except Exception as exc:
        logger.error(f"Error making prediction: {exc}")
        raise self.retry(exc=exc, countdown=30, max_retries=2)


@shared_task(bind=True, name='ai_ml.tasks.analyze_image')
def analyze_image(self, image_data, analysis_type, user_id, location=None):
    """
    Analyze an image using computer vision models.
    
    Args:
        image_data: Base64 encoded image data
        analysis_type: Type of analysis to perform
        user_id: ID of the user requesting analysis
        location: Optional location information
    """
    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Processing image...'}
        )
        
        # Get user
        user = User.objects.get(id=user_id)
        
        # Decode image data
        try:
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            raise ValueError(f"Invalid image data: {e}")
        
        # Simulate image processing
        time.sleep(1.0)
        
        # Generate mock analysis results based on type
        if analysis_type == 'crop_health':
            analysis_result = {
                'overall_health': np.random.choice(['excellent', 'good', 'fair', 'poor']),
                'health_score': round(np.random.uniform(0.6, 1.0), 2),
                'issues_detected': np.random.choice([0, 1, 2, 3]),
                'recommendations': ['Continue current practices', 'Monitor for changes', 'Consider fertilization']
            }
            detected_objects = ['healthy_leaves', 'green_stems', 'normal_growth']
            
        elif analysis_type == 'disease_detection':
            analysis_result = {
                'diseases_detected': np.random.choice([0, 1, 2]),
                'severity': np.random.choice(['none', 'mild', 'moderate', 'severe']),
                'affected_area_percentage': round(np.random.uniform(0, 30), 1),
                'treatment_recommendations': ['Remove affected leaves', 'Apply fungicide', 'Improve air circulation']
            }
            detected_objects = ['healthy_leaves', 'diseased_spots', 'yellowed_areas']
            
        elif analysis_type == 'pest_detection':
            analysis_result = {
                'pests_detected': np.random.choice([0, 1, 2, 3]),
                'infestation_level': np.random.choice(['none', 'low', 'moderate', 'high']),
                'pest_types': np.random.choice(['aphids', 'spider_mites', 'whiteflies'], size=np.random.randint(0, 3)),
                'control_measures': ['Apply insecticide', 'Introduce beneficial insects', 'Remove affected plants']
            }
            detected_objects = ['healthy_plant', 'pest_insects', 'damaged_leaves']
            
        else:
            analysis_result = {
                'analysis_complete': True,
                'confidence': round(np.random.uniform(0.7, 0.95), 2)
            }
            detected_objects = ['general_objects']
        
        # Generate confidence scores for detected objects
        confidence_scores = {
            obj: round(np.random.uniform(0.7, 0.95), 2) 
            for obj in detected_objects
        }
        
        # Create computer vision analysis record
        cv_analysis = ComputerVisionAnalysis.objects.create(
            user=user,
            analysis_type=analysis_type,
            image=image_data,  # Store as base64 for demo
            analysis_result=analysis_result,
            detected_objects=detected_objects,
            confidence_scores=confidence_scores,
            processing_time=1.0,
            model_version='v1.0.0',
            location=location
        )
        
        logger.info(f"Image analysis completed: {cv_analysis.id}")
        
        return {
            'analysis_id': str(cv_analysis.id),
            'analysis_result': analysis_result,
            'detected_objects': detected_objects,
            'processing_time': 1.0
        }
        
    except Exception as exc:
        logger.error(f"Error analyzing image: {exc}")
        raise self.retry(exc=exc, countdown=30, max_retries=2)


@shared_task(bind=True, name='ai_ml.tasks.generate_recommendations')
def generate_recommendations(self, user_id, context_data=None):
    """
    Generate AI-powered recommendations for a user.
    
    Args:
        user_id: ID of the user to generate recommendations for
        context_data: Optional context data for recommendations
    """
    try:
        # Get user
        user = User.objects.get(id=user_id)
        
        # Simulate recommendation generation
        time.sleep(0.5)
        
        # Generate mock recommendations based on context
        recommendations = []
        
        # Crop selection recommendation
        recommendations.append({
            'type': 'crop_selection',
            'title': 'Optimal Crop Selection for Current Season',
            'description': 'Based on soil analysis and weather forecasts, consider planting maize or soybeans this season.',
            'priority': 'high',
            'confidence_score': round(np.random.uniform(0.8, 0.95), 2),
            'action_items': ['Prepare soil for maize', 'Purchase quality seeds', 'Plan irrigation schedule'],
            'expected_benefits': 'Expected 15-20% increase in yield compared to previous crops'
        })
        
        # Irrigation schedule recommendation
        recommendations.append({
            'type': 'irrigation_schedule',
            'title': 'Optimized Irrigation Schedule',
            'description': 'Adjust irrigation frequency based on recent weather patterns and soil moisture levels.',
            'priority': 'medium',
            'confidence_score': round(np.random.uniform(0.7, 0.9), 2),
            'action_items': ['Reduce irrigation frequency by 20%', 'Monitor soil moisture sensors', 'Adjust timing to early morning'],
            'expected_benefits': 'Water savings of 25% while maintaining crop health'
        })
        
        # Pest control recommendation
        if np.random.random() > 0.5:
            recommendations.append({
                'type': 'pest_control',
                'title': 'Preventive Pest Control Measures',
                'description': 'Early detection and prevention of common pests in your crop area.',
                'priority': 'medium',
                'confidence_score': round(np.random.uniform(0.7, 0.85), 2),
                'action_items': ['Apply preventive insecticide', 'Install pheromone traps', 'Regular field monitoring'],
                'expected_benefits': 'Prevent potential 10-15% yield loss due to pest damage'
            })
        
        # Create recommendation records
        created_recommendations = []
        for rec_data in recommendations:
            recommendation = Recommendation.objects.create(
                user=user,
                recommendation_type=rec_data['type'],
                priority=rec_data['priority'],
                title=rec_data['title'],
                description=rec_data['description'],
                action_items=rec_data['action_items'],
                expected_benefits=rec_data['expected_benefits'],
                confidence_score=rec_data['confidence_score'],
                reasoning='Generated based on historical data, current conditions, and predictive models',
                supporting_data={
                    'weather_data': 'recent_forecasts',
                    'soil_data': 'laboratory_analysis',
                    'market_data': 'price_trends',
                    'historical_yields': 'previous_seasons'
                },
                expires_at=timezone.now() + timedelta(days=60)
            )
            created_recommendations.append(recommendation)
        
        logger.info(f"Generated {len(created_recommendations)} recommendations for user {user_id}")
        
        return {
            'recommendations_created': len(created_recommendations),
            'recommendation_ids': [str(r.id) for r in created_recommendations]
        }
        
    except Exception as exc:
        logger.error(f"Error generating recommendations: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=2)


@shared_task(bind=True, name='ai_ml.tasks.retrain_models')
def retrain_models(self, model_types=None):
    """
    Retrain AI models based on new data and performance metrics.
    
    Args:
        model_types: Optional list of model types to retrain
    """
    try:
        # Get models to retrain
        if model_types:
            models = AIModel.objects.filter(
                model_type__in=model_types,
                status__in=['active', 'inactive']
            )
        else:
            # Retrain models that haven't been trained recently
            cutoff_date = timezone.now() - timedelta(days=30)
            models = AIModel.objects.filter(
                last_trained__lt=cutoff_date,
                status__in=['active', 'inactive']
            )
        
        retrained_count = 0
        
        for model in models:
            try:
                # Create training job
                training_job = TrainingJob.objects.create(
                    model=model,
                    status='pending',
                    training_config={'epochs': 100, 'batch_size': 32},
                    total_epochs=100
                )
                
                # Trigger training task
                train_model.delay(str(model.id))
                retrained_count += 1
                
            except Exception as e:
                logger.error(f"Error scheduling retraining for model {model.id}: {e}")
                continue
        
        logger.info(f"Scheduled retraining for {retrained_count} models")
        
        return {
            'models_scheduled': retrained_count,
            'total_models': models.count()
        }
        
    except Exception as exc:
        logger.error(f"Error in model retraining: {exc}")
        raise self.retry(exc=exc, countdown=300, max_retries=3)


@shared_task(bind=True, name='ai_ml.tasks.cleanup_old_data')
def cleanup_old_data(self, days_old=90):
    """
    Clean up old AI/ML data to maintain database performance.
    
    Args:
        days_old: Age threshold for data cleanup in days
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=days_old)
        
        # Clean up old predictions
        old_predictions = Prediction.objects.filter(created_at__lt=cutoff_date)
        predictions_deleted = old_predictions.count()
        old_predictions.delete()
        
        # Clean up old computer vision analyses
        old_cv_analyses = ComputerVisionAnalysis.objects.filter(created_at__lt=cutoff_date)
        cv_analyses_deleted = old_cv_analyses.count()
        old_cv_analyses.delete()
        
        # Clean up old recommendations
        old_recommendations = Recommendation.objects.filter(
            created_at__lt=cutoff_date,
            is_applied=True
        )
        recommendations_deleted = old_recommendations.count()
        old_recommendations.delete()
        
        # Clean up old training jobs
        old_training_jobs = TrainingJob.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['completed', 'failed', 'cancelled']
        )
        training_jobs_deleted = old_training_jobs.count()
        old_training_jobs.delete()
        
        total_deleted = predictions_deleted + cv_analyses_deleted + recommendations_deleted + training_jobs_deleted
        
        logger.info(f"Cleaned up {total_deleted} old AI/ML records")
        
        return {
            'predictions_deleted': predictions_deleted,
            'cv_analyses_deleted': cv_analyses_deleted,
            'recommendations_deleted': recommendations_deleted,
            'training_jobs_deleted': training_jobs_deleted,
            'total_deleted': total_deleted
        }
        
    except Exception as exc:
        logger.error(f"Error in data cleanup: {exc}")
        raise self.retry(exc=exc, countdown=600, max_retries=2)


@shared_task(bind=True, name='ai_ml.tasks.update_model_performance')
def update_model_performance(self):
    """Update performance metrics for all active AI models."""
    try:
        active_models = AIModel.objects.filter(status='active')
        updated_count = 0
        
        for model in active_models:
            try:
                # Simulate performance update
                time.sleep(0.1)
                
                # Update metrics with slight variations
                if model.accuracy:
                    model.accuracy = max(0.5, min(1.0, model.accuracy + np.random.uniform(-0.05, 0.05)))
                    model.precision = max(0.5, min(1.0, model.precision + np.random.uniform(-0.05, 0.05)))
                    model.recall = max(0.5, min(1.0, model.recall + np.random.uniform(-0.05, 0.05)))
                    model.f1_score = 2 * (model.precision * model.recall) / (model.precision + model.recall)
                    model.save()
                    updated_count += 1
                    
            except Exception as e:
                logger.error(f"Error updating model {model.id}: {e}")
                continue
        
        logger.info(f"Updated performance metrics for {updated_count} models")
        
        return {
            'models_updated': updated_count,
            'total_models': active_models.count()
        }
        
    except Exception as exc:
        logger.error(f"Error updating model performance: {exc}")
        raise self.retry(exc=exc, countdown=300, max_retries=2)

