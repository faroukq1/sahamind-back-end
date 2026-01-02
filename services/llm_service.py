from transformers import pipeline
import torch

# Load emotion classification model once at startup
_emotion_classifier = None

def get_emotion_classifier():
    global _emotion_classifier
    if _emotion_classifier is None:
        # This model is specifically trained for emotion detection
        _emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,  # Return all emotions with probabilities
            device=0 if torch.cuda.is_available() else -1  # Use GPU if available
        )
    return _emotion_classifier


def analyze_emotions(text: str) -> dict[str, float]:
    """
    Analyze emotions using a pre-trained BERT model.
    Returns a dictionary mapping emotions to probabilities.
    """
    try:
        classifier = get_emotion_classifier()
        results = classifier(text)[0]  # Get first result
        
        # Convert to your format
        emotions = {}
        for item in results:
            label = item['label'].lower()
            score = item['score']
            
            # Map model labels to your required emotions
            # Model outputs: anger, disgust, fear, joy, neutral, sadness, surprise
            label_mapping = {
                'anger': 'anger',
                'fear': 'fear',
                'sadness': 'sadness',
                'joy': 'loneliness',  # Map as needed
                'disgust': 'burnout',  # Map as needed
                'surprise': 'anxiety',  # Map as needed
                'neutral': 'anxiety'
            }
            
            mapped_label = label_mapping.get(label, label)
            
            # If your required emotions only
            if mapped_label in ['anxiety', 'burnout', 'sadness', 'anger', 'fear', 'loneliness']:
                emotions[mapped_label] = emotions.get(mapped_label, 0.0) + score
        
        # Normalize to sum to 1
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        else:
            emotions = {"anxiety": 1.0}
            
        return emotions
        
    except Exception as e:
        print(f"Error analyzing emotions: {e}")
        return {"anxiety": 1.0}