"""
Intent Classifier for Chatbot Testing
Provides utility functions for intent classification and validation
Author: Mira Mamdoh
"""

from typing import List, Dict, Tuple


class IntentClassifier:
    """Utility class for intent classification and evaluation"""
    
    @staticmethod
    def calculate_accuracy(predictions: List[str], ground_truth: List[str]) -> float:
        """
        Calculate classification accuracy
        
        Args:
            predictions: List of predicted intents
            ground_truth: List of actual intents
            
        Returns:
            Accuracy score (0.0 to 1.0)
        """
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have same length")
        
        if len(predictions) == 0:
            return 0.0
        
        correct = sum(1 for pred, true in zip(predictions, ground_truth) if pred == true)
        return correct / len(predictions)
    
    @staticmethod
    def get_confusion_matrix(predictions: List[str], 
                           ground_truth: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Generate confusion matrix for intent classification
        
        Args:
            predictions: List of predicted intents
            ground_truth: List of actual intents
            
        Returns:
            Nested dict representing confusion matrix
        """
        matrix = {}
        
        for pred, true in zip(predictions, ground_truth):
            if true not in matrix:
                matrix[true] = {}
            if pred not in matrix[true]:
                matrix[true][pred] = 0
            matrix[true][pred] += 1
        
        return matrix
    
    @staticmethod
    def calculate_precision_recall(predictions: List[str],
                                  ground_truth: List[str],
                                  intent: str) -> Tuple[float, float]:
        """
        Calculate precision and recall for a specific intent
        
        Args:
            predictions: List of predicted intents
            ground_truth: List of actual intents
            intent: The intent to calculate metrics for
            
        Returns:
            Tuple of (precision, recall)
        """
        true_positive = sum(1 for pred, true in zip(predictions, ground_truth)
                          if pred == intent and true == intent)
        false_positive = sum(1 for pred, true in zip(predictions, ground_truth)
                           if pred == intent and true != intent)
        false_negative = sum(1 for pred, true in zip(predictions, ground_truth)
                           if pred != intent and true == intent)
        
        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0.0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0.0
        
        return precision, recall
    
    @staticmethod
    def get_intent_distribution(intents: List[str]) -> Dict[str, int]:
        """
        Get distribution of intents
        
        Args:
            intents: List of intent labels
            
        Returns:
            Dict mapping intent to count
        """
        distribution = {}
        for intent in intents:
            distribution[intent] = distribution.get(intent, 0) + 1
        return distribution