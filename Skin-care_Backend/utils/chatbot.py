"""
Hybrid Chatbot with RapidFuzz + FREE HuggingFace Models
NO API COSTS - 100% FREE!
"""
from rapidfuzz import fuzz, process
import json
from transformers import pipeline
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch    

class HybridChatbot:
    def __init__(self, knowledge_file, similarity_threshold=75):
        """
        Initialize hybrid chatbot with FREE HuggingFace models
        """
        self.similarity_threshold = similarity_threshold
        
        # Load knowledge base
        print(f"📚 Loading knowledge base from {knowledge_file}...")
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.qa_database = data['qa_database']
        self.metadata = data.get('metadata', {})
        
        # Build question bank for fuzzy matching
        self.question_bank = []
        self.question_map = {}
        
        for qa in self.qa_database:
            question = qa['question']
            tags = qa.get('tags', [])
            
            self.question_bank.append(question)
            self.question_map[question] = qa
            
            for tag in tags:
                self.question_bank.append(tag)
                self.question_map[tag] = qa
        
        print(f"✅ Loaded {len(self.qa_database)} Q&A pairs")
        print(f"✅ Total searchable items: {len(self.question_bank)}")
        
        # Load FREE HuggingFace model
        self.tokenizer = None
        self.huggingface_model = None
        
        try:
            print("🤖 Loading FREE HuggingFace model (Seq2Seq)...")
            model_id = "facebook/blenderbot-400M-distill"
            
            # Load tokenizer and model separately to avoid "Unknown Task" errors
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.huggingface_model = AutoModelForSeq2SeqLM.from_pretrained(
                model_id,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32 # Use float16 if you have a GPU
            )
            
            print("✅ Model and Tokenizer loaded successfully!")
        
        except Exception as e:
            print(f"⚠️ Loading failed: {e}")
    
    def find_best_match(self, user_question):
        """Find best matching Q&A using RapidFuzz"""
        result = process.extractOne(
            user_question.lower(),
            self.question_bank,
            scorer=fuzz.WRatio
        )
        
        if result:
            matched_text, score, _ = result
            qa_data = self.question_map.get(matched_text)
            if qa_data:
                return qa_data, score
        return None, 0
    
    def format_answer(self, qa_data):
        """Format stored answer with related questions"""
        answer = qa_data['answer']
        related = qa_data.get('related_questions', [])
        if related:
            answer += "\n\n**Related Questions:**"
            for r in related:
                answer += f"\n• {r}"
        return answer
    
    def generate_ai_response(self, user_question, skin_type=None):
        # 1. DEFINE PROMPT IMMEDIATELY (Fixes the NameError)
        prompt = user_question 
        question_lower = user_question.lower()
        relevant_snippets = []
        
        # 2. Search for Skincare Context
        for qa in self.qa_database:
            if any(tag in question_lower for tag in qa.get('tags', [])):
                lines = qa['answer'].split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('**'):
                        relevant_snippets.append(line.strip())
                        break
        
        # 3. Update prompt ONLY if context is found
        if relevant_snippets:
            skin_info = f"User has {skin_type} skin. " if skin_type else ""
            context_text = "Context: " + " | ".join(relevant_snippets[:2]) + ". "
            prompt = f"{skin_info}{context_text}Question: {user_question}"
        
        # 4. MANUAL GENERATION (The APJ fix)
        if self.huggingface_model and self.tokenizer:
            try:
                print(f"🤖 AI is thinking about: {user_question}")
                
                # Manual Encoding
                inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
                
                # Manual Generation - Bypasses all pipeline errors
                output_tokens = self.huggingface_model.generate(
                    **inputs,
                    max_new_tokens=80,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
                
                # Manual Decoding
                generated = self.tokenizer.batch_decode(output_tokens, skip_special_tokens=True)[0]
                
                if generated:
                    return generated.strip()
                        
            except Exception as e:
                # This will now catch actual model errors, not variable errors
                print(f"⚠️ Manual Generation Error: {e}")
        
        # 5. Final Fallback (If AI fails, show the menu)
        return self._fallback_response(user_question, skin_type)
    
    def _fallback_response(self, user_question, skin_type=None):
        question_lower = user_question.lower()
        responses = {
            'acne': "For acne, I recommend tea tree oil, honey masks, or salicylic acid. Keep your skin clean!",
            'dark circles': "Try cold cucumber slices or caffeine eye creams. Sleep is key!",
            'dry': "For dry skin, focus on hydration! Use hyaluronic acid and rich moisturizers.",
            'oily': "Use gel cleansers and oil-free products. Try niacinamide.",
            'wrinkles': "Retinol and SPF 50 are the best for wrinkles!",
            'pigmentation': "Vitamin C serum and SPF 50 work great for dark spots.",
            'sunscreen': "SPF 50 daily is essential! Reapply every 2 hours.",
            'routine': f"For {skin_type or 'your'} skin, I recommend: cleanser, toner, serum, moisturizer, and SPF."
        }
        
        for topic, response in responses.items():
            if topic in question_lower:
                return response
        
        skin_context = f" for {skin_type} skin" if skin_type else ""
        return f"I'm your AI Skincare Assistant{skin_context}! I can help with acne, routines, and product tips. Could you be more specific about your skin concern?"
    
    def get_response(self, user_question, skin_type=None):
        matched_qa, similarity_score = self.find_best_match(user_question)
        print(f"🔍 Fuzzy match score: {similarity_score}%")
        
        if similarity_score >= self.similarity_threshold and matched_qa:
            return {
                "answer": self.format_answer(matched_qa),
                "source": "stored",
                "similarity_score": similarity_score,
                "matched_question": matched_qa['question'],
                "confidence": "high"
            }
        
        ai_answer = self.generate_ai_response(user_question, skin_type)
        return {
            "answer": ai_answer,
            "source": "ai_generated",
            "similarity_score": similarity_score,
            "confidence": "medium"
        }