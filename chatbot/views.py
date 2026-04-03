from django.shortcuts import render
from django.http import JsonResponse
import json

def chat_respond(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Simple rule-based logic
            response = "Je ne suis pas sûr de comprendre votre question. Pourriez-vous préciser ? Vous pouvez me poser des questions sur les inscriptions, les horaires ou les tarifs."
            
            if "horaire" in user_message or "temps" in user_message:
                response = "Les cours commencent généralement à 8h00 et se terminent à 16h30 du lundi au vendredi. Le samedi, les activités se terminent à 12h00."
            elif "inscription" in user_message or "inscrire" in user_message:
                response = "Pour les inscriptions, vous devez fournir un acte de naissance, les bulletins de l'année précédente et 4 photos d'identité. Le bureau d'admission est ouvert de 9h à 15h."
            elif "tarif" in user_message or "frais" in user_message or "prix" in user_message:
                response = "Nos tarifs varient selon le niveau scolaire. Je vous invite à consulter la section 'Frais de scolarité' sur votre tableau de bord ou à contacter la comptabilité."
            elif "contact" in user_message or "appeler" in user_message:
                response = "Vous pouvez nous contacter au +212 5XX XX XX XX ou par email à contact@preskool.com."
            elif "bonjour" in user_message or "salut" in user_message:
                response = "Bonjour ! Je suis l'assistant virtuel de PreSkool. Comment puis-je vous aider aujourd'hui ?"
            
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
