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
      <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Finalizar Compra
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

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Produto */}
            <div>
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Resumo do pedido</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-4">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold">{product.name}</h3>
                      <p className="text-gray-600 text-sm">{product.description}</p>
                      <p className="text-2xl font-bold text-orange-500 mt-2">
                        {product.price}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Dados do cliente */}
              <Card>
                <CardHeader>
                  <CardTitle>Seus dados</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="name">Nome completo *</Label>
                    <Input
                      id="name"
                      name="name"
                      value={customerData.name}
                      onChange={handleInputChange}
                      placeholder="João Silva"
                      disabled={isLoading}
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">E-mail *</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={customerData.email}
                      onChange={handleInputChange}
                      placeholder="joao@email.com"
                      disabled={isLoading}
                    />
                  </div>
                  <div>
                    <Label htmlFor="document">CPF/CNPJ *</Label>
                    <Input
                      id="document"
                      name="document"
                      value={customerData.document}
                      onChange={handleInputChange}
                      placeholder="123.456.789-00"
                      disabled={isLoading}
                    />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Pagamento */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Forma de pagamento</CardTitle>
                </CardHeader>
                <CardContent>
                  {/* Tabs de pagamento */}
                  <div className="flex space-x-2 mb-6">
                    <Button
                      variant={selectedMethod === 'pix' ? 'default' : 'outline'}
                      onClick={() => setSelectedMethod('pix')}
                      className="flex-1"
                      disabled={isLoading}
                    >
                      <Smartphone className="mr-2 h-4 w-4" />
                      PIX
                    </Button>
                    <Button
                      variant={selectedMethod === 'credit_card' ? 'default' : 'outline'}
                      onClick={() => setSelectedMethod('credit_card')}
                      className="flex-1"
                      disabled={isLoading}
                    >
                      <CreditCard className="mr-2 h-4 w-4" />
                      Cartão
                    </Button>
                    <Button
                      variant={selectedMethod === 'boleto' ? 'default' : 'outline'}
                      onClick={() => setSelectedMethod('boleto')}
                      className="flex-1"
                      disabled={isLoading}
                    >
                      <FileText className="mr-2 h-4 w-4" />
                      Boleto
                    </Button>
                  </div>

                  {/* PIX */}
                  {selectedMethod === 'pix' && (
                    <div>
                      {!paymentResult ? (
                        <div className="text-center">
                          <p className="text-gray-600 mb-4">
                            Pagamento instantâneo via PIX
                          </p>
                          <Button
                            onClick={handlePixPayment}
                            disabled={isLoading}
                            className="bg-orange-500 hover:bg-orange-600"
                          >
                            {isLoading ? (
                              <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Gerando PIX...
                              </>
                            ) : (
                              'Gerar PIX'
                            )}
                          </Button>
                        </div>
                      ) : (
                        <div className="text-center">
                          <div className="mb-4 bg-gray-100 p-8 rounded-lg">
                            <p className="text-lg font-semibold mb-2">PIX QR Code</p>
                            <p className="text-sm text-gray-600">Use seu app do banco para escanear</p>
                          </div>
                          <p className="text-sm text-gray-600 mb-4">
                            Escaneie o QR Code com seu banco ou copie o código
                          </p>
                          <div className="bg-gray-100 p-3 rounded mb-4">
                            <code className="text-xs break-all">{qrCode}</code>
                          </div>
                          <Button onClick={copyPixCode} variant="outline">
                            Copiar código PIX
                          </Button>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Cartão de crédito */}
                  {selectedMethod === 'credit_card' && (
                    <div>
                      {installmentOptions.length > 0 && (
                        <div className="mb-4">
                          <Label>Parcelamento</Label>
                          <select
                            value={selectedInstallments}
                            onChange={(e) => setSelectedInstallments(parseInt(e.target.value))}
                            className="w-full p-2 border rounded"
                            disabled={isLoading}
                          >
                            {installmentOptions.map((option) => (
                              <option key={option.installments} value={option.installments}>
                                {option.recommended_message || `${option.installments}x de R$ ${option.installment_amount?.toFixed(2)}`}
                              </option>
                            ))}
                          </select>
                        </div>
                      )}
                      
                      <CardPayment
                        initialization={{
                          amount: parseFloat(product.price.replace('R$ ', '').replace(',', '.')),
                          payer: {
                            email: customerData.email || undefined
                          }
                        }}
                        customization={{
                          paymentMethods: {
                            creditCard: 'all',
                            debitCard: 'all'
                          }
                        }}
                        onSubmit={handleCardPayment}
                        onReady={() => console.log('Card payment ready')}
                        onError={(error) => {
                          console.error('Card payment error:', error);
                          toast({
                            title: "Erro",
                            description: "Erro no formulário do cartão",
                            variant: "destructive"
                          });
                        }}
                      />
                    </div>
                  )}

                  {/* Boleto */}
                  {selectedMethod === 'boleto' && (
                    <div>
                      {!paymentResult ? (
                        <div className="text-center">
                          <p className="text-gray-600 mb-4">
                            Vencimento em 7 dias úteis
                          </p>
                          <Button
                            onClick={handleBoletoPayment}
                            disabled={isLoading}
                            className="bg-orange-500 hover:bg-orange-600"
                          >
                            {isLoading ? (
                              <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Gerando boleto...
                              </>
                            ) : (
                              'Gerar Boleto'
                            )}
                          </Button>
                        </div>
                      ) : (
                        <div className="text-center">
                          <p className="text-green-600 font-semibold mb-4">
                            Boleto gerado com sucesso!
                          </p>
                          <Button
                            onClick={() => window.open(paymentResult.ticket_url, '_blank')}
                            className="bg-blue-500 hover:bg-blue-600"
                          >
                            Visualizar Boleto
                          </Button>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};