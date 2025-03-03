from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from dotenv import load_dotenv
import os
import mercadopago

load_dotenv()

pagamento_bp = Blueprint("pagamento_bp", __name__)

MERCADO_PAGO_PUBLIC_KEY = os.getenv("MERCADO_PAGO_PUBLIC_KEY")
MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

@pagamento_bp.route("/pagamento")
@login_required
def pagamento():
    plano_selecionado = session.get('plano_selecionado', {})
    
    if not plano_selecionado:
        return redirect(url_for('planos_bp.planos'))
        
    return render_template(
        "pagamento.html",
        public_key=MERCADO_PAGO_PUBLIC_KEY,
        plano=plano_selecionado
    )

@pagamento_bp.route("/process_payment", methods=['POST'])
@login_required
def process_payment():
    try:
        request_values = request.get_json()
        
        payment_data = {
            "transaction_amount": float(request_values.get("transaction_amount")),
            "token": request_values.get("token"),
            "installments": int(request_values.get("installments")),
            "payment_method_id": request_values.get("payment_method_id"),
            "payer": {
                "email": current_user.email,
                "identification": {
                    "type": request_values.get("payer", {}).get("identification", {}).get("type"),
                    "number": request_values.get("payer", {}).get("identification", {}).get("number")
                }
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        return jsonify({
            "id": payment["id"],
            "status": payment["status"],
            "detail": payment["status_detail"]
        })

    except Exception as e:
        return jsonify({
            "error_message": str(e)
        }), 400
