import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { X, MessageCircle, ShoppingCart, User } from 'lucide-react';
import { whatsappAPI } from '../services/api';

export const PaymentModal = ({ product, isOpen, onClose, onSuccess }) => {
  const [quantity, setQuantity] = useState(1);
  const [customerName, setCustomerName] = useState('');

  const handleWhatsAppPurchase = () => {
    // Enviar dados do produto e quantidade para WhatsApp
    whatsappAPI.buyProduct(product, quantity);
    
    // Fechar modal e mostrar sucesso
    onClose();
    
    // Callback de sucesso (se necessário)
    if (onSuccess) {
      onSuccess({
        product: product,
        quantity: quantity,
        method: 'whatsapp',
        customer_name: customerName
      });
    }
  };

  const getTotalPrice = () => {
    const price = parseFloat(product.price.replace('R$ ', '').replace(',', '.'));
    const total = price * quantity;
    return `R$ ${total.toFixed(2).replace('.', ',')}`;
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Finalizar Pedido
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="p-2"
            >
              <X className="h-6 w-6" />
            </Button>
          </div>

          {/* Produto */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="h-5 w-5" />
                Resumo do pedido
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-4">
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-20 h-20 object-cover rounded-lg"
                />
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{product.name}</h3>
                  <p className="text-gray-600 text-sm mb-2">{product.description}</p>
                  <p className="text-2xl font-bold text-blue-500">
                    {product.price}
                  </p>
                </div>
              </div>

              {/* Quantidade */}
              <div className="mt-4 pt-4 border-t">
                <Label htmlFor="quantity" className="text-sm font-medium">
                  Quantidade:
                </Label>
                <div className="flex items-center mt-2 space-x-3">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  >
                    -
                  </Button>
                  <Input
                    id="quantity"
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-20 text-center"
                  />
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(quantity + 1)}
                  >
                    +
                  </Button>
                </div>
                {quantity > 1 && (
                  <p className="text-sm text-gray-600 mt-2">
                    Total: <span className="font-semibold">{getTotalPrice()}</span>
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Dados básicos */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Seu nome (opcional)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Input
                placeholder="Digite seu nome para personalizar a mensagem"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
              />
            </CardContent>
          </Card>

          {/* WhatsApp */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageCircle className="h-5 w-5" />
                Finalizar via WhatsApp
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
                  <p className="text-sm text-gray-600 mb-2">
                    Ao clicar no botão abaixo, você será redirecionado para o WhatsApp 
                    com uma mensagem já preenchida contendo os detalhes do seu pedido.
                  </p>
                  <p className="text-xs text-green-600 font-medium">
                    ✓ Atendimento personalizado<br />
                    ✓ Negociação de preço e prazo<br />
                    ✓ Esclarecimento de dúvidas<br />
                    ✓ Formas de pagamento flexíveis
                  </p>
                </div>
                
                <Button
                  onClick={handleWhatsAppPurchase}
                  className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3"
                  size="lg"
                >
                  <MessageCircle className="mr-2 h-5 w-5" />
                  Finalizar no WhatsApp
                </Button>
                
                <p className="text-xs text-gray-500 mt-3">
                  Você será redirecionado para o WhatsApp Web ou app
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};