"""
API Testing Script
Run this to test all endpoints
"""
import requests
import json
import os

# Configuration
BASE_URL = "http://localhost:5000"
TEST_IMAGE_PATH = "tests/test_images/test_face.jpg"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("🏥 Testing Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    print("✅ Health check passed!")

def test_disease_detection():
    """Test disease detection endpoint"""
    print("\n" + "="*60)
    print("🔬 Testing Disease Detection")
    print("="*60)
    
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        print("   Please add a test image to tests/test_images/")
        return
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{BASE_URL}/api/disease/analyze", files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['success'] == True
    print("✅ Disease detection passed!")

def test_skincare_analysis():
    """Test skincare analysis endpoint"""
    print("\n" + "="*60)
    print("🧴 Testing Skincare Analysis")
    print("="*60)
    
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        return
    
    # Prepare questionnaire
    questionnaire = {
        "concerns": ["Acne", "Dark Circles"],
        "sleep_hours": "5-6 hours",
        "water_intake": "3-5 glasses",
        "stress_level": "Moderate",
        "sun_exposure": "Moderate",
        "diet": "Mixed"
    }
    
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'image': f}
        data = {'questionnaire': json.dumps(questionnaire)}
        response = requests.post(
            f"{BASE_URL}/api/skincare/analyze",
            files=files,
            data=data
        )
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    if result.get('success'):
        print(f"Skin Type: {result['ai_analysis']['skin_type']}")
        print(f"Confidence: {result['ai_analysis']['confidence']:.2f}%")
        print(f"Concerns: {result['user_input']['concerns']}")
        print(f"Morning Routine Steps: {len(result['personalized_routine']['morning'])}")
    
    print(f"\nFull Response: {json.dumps(result, indent=2)[:500]}...")
    
    assert response.status_code == 200
    assert result['success'] == True
    print("✅ Skincare analysis passed!")

def test_chatbot():
    """Test chatbot endpoint"""
    print("\n" + "="*60)
    print("💬 Testing Chatbot")
    print("="*60)
    
    test_questions = [
        {"message": "how to treat acne", "skin_type": "Oily"},
        {"message": "what causes dark circles", "skin_type": None},
        {"message": "best sunscreen for dry skin", "skin_type": "Dry"}
    ]
    
    for idx, question in enumerate(test_questions, 1):
        print(f"\n--- Test {idx} ---")
        print(f"Question: {question['message']}")
        
        response = requests.post(
            f"{BASE_URL}/api/chatbot/chat",
            json=question
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"Source: {result['source']}")
            print(f"Similarity: {result['similarity_score']}%")
            print(f"Answer: {result['message'][:200]}...")
        else:
            print(f"Error: {result.get('error')}")
        
        assert response.status_code == 200
        assert result['success'] == True
    
    print("\n✅ Chatbot tests passed!")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 RUNNING ALL API TESTS")
    print("="*60)
    
    try:
        test_health()
        test_disease_detection()
        test_skincare_analysis()
        test_chatbot()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
    
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to {BASE_URL}")
        print("   Make sure the Flask server is running!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    run_all_tests()