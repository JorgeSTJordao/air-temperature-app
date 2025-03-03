// Inicialização imediata do Mercado Pago
const mercadoPagoPublicKey = document.getElementById("mercado-pago-public-key").value;
const mercadopago = new MercadoPago(mercadoPagoPublicKey);
let cardPaymentBrickController;

// Função para mostrar/esconder o loading
function toggleLoading(show) {
    document.getElementById('loading-container').style.display = show ? 'flex' : 'none';
    document.getElementById('mercadopago-bricks-contaner__PaymentCard').style.display = show ? 'none' : 'block';
}

// Carrega o formulário imediatamente
(async function loadPaymentForm() {
    const productCost = document.getElementById('amount').value;
    const settings = {
        initialization: {
            amount: productCost,
        },
        callbacks: {
            onReady: () => {
                console.log('brick ready');
                toggleLoading(false);
                // Adiciona CSS customizado após o carregamento
                const style = document.createElement('style');
                style.textContent = `
                    .mp-brick-form > div:last-child {
                        display: flex !important;
                        justify-content: flex-end !important;
                    }
                    .mp-button-content {
                        width: auto !important;
                    }
                    form[data-initialized="true"] > div:last-child {
                        display: flex !important;
                        justify-content: flex-end !important;
                    }
                `;
                document.head.appendChild(style);
            },
            onError: (error) => {
                console.error(error);
                alert('Erro ao processar pagamento: ' + JSON.stringify(error));
                toggleLoading(false);
            },
            onSubmit: (cardFormData) => {
                proccessPayment(cardFormData);
            }
        },
        locale: 'pt-BR',
        customization: {
            paymentMethods: {
                maxInstallments: 12
            },
            visual: {
                style: {
                    theme: 'default',
                    customVariables: {
                        formBackgroundColor: '#ffffff',
                        baseColor: '#0F468C'
                    }
                }
            }
        },
    };

    try {
        const bricks = mercadopago.bricks();
        cardPaymentBrickController = await bricks.create('cardPayment', 'mercadopago-bricks-contaner__PaymentCard', settings);
    } catch (error) {
        console.error('Erro ao carregar formulário:', error);
        toggleLoading(false);
        alert('Erro ao carregar o formulário de pagamento. Por favor, recarregue a página.');
    }
})();

const proccessPayment = (cardFormData) => {
    toggleLoading(true);
    
    fetch("/process_payment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(cardFormData)
    })
    .then(response => response.json())
    .then(result => {
        toggleLoading(false);
        
        if(!result.hasOwnProperty("error_message")) {
            document.querySelector(".payment-form").style.display = "none";
            document.querySelector(".payment-result").style.display = "block";
            
            document.getElementById("payment-id").innerText = result.id;
            document.getElementById("payment-status").innerText = result.status;
            document.getElementById("payment-detail").innerText = result.detail;
        } else {
            alert("Erro no pagamento:\n" + result.error_message);
        }
    })
    .catch(error => {
        console.error(error);
        toggleLoading(false);
        alert("Erro inesperado ao processar pagamento");
    });
}; 