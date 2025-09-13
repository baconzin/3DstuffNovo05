import React, { useState, useEffect } from 'react';
import { MessageCircle, X, Clock, Users } from 'lucide-react';

export const WhatsAppBanner = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);

  const whatsappNumber = "5519971636969"; // Número real do cliente

  useEffect(() => {
    // Mostrar banner após 5 segundos
    const timer = setTimeout(() => {
      if (!isDismissed) {
        setIsVisible(true);
      }
    }, 5000);

    return () => clearTimeout(timer);
  }, [isDismissed]);

  const handleWhatsAppClick = () => {
    const message = "Olá! 👋 Vi o banner no site da 3D Stuff e gostaria de falar sobre os produtos de impressão 3D!";
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
    setIsVisible(false);
  };

  const handleDismiss = () => {
    setIsVisible(false);
    setIsDismissed(true);
  };

  if (!isVisible || isDismissed) return null;

  return (
    <div className={`fixed bottom-0 left-0 right-0 z-50 transform transition-all duration-300 ${
      isVisible ? 'translate-y-0' : 'translate-y-full'
    }`}>
      <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            {/* Conteúdo principal */}
            <div className="flex items-center space-x-4">
              <div className="relative">
                <MessageCircle className="h-8 w-8" />
                <div className="absolute -top-1 -right-1 bg-green-300 rounded-full h-3 w-3 animate-ping"></div>
              </div>
              
              <div className="flex-1">
                <h3 className="font-bold text-lg">💬 Dúvidas sobre nossos produtos?</h3>
                <p className="text-green-100 text-sm">
                  Fale conosco no WhatsApp e tire todas suas dúvidas sobre impressão 3D!
                </p>
              </div>

              {/* Status online */}
              <div className="hidden md:flex items-center space-x-4 text-green-100">
                <div className="flex items-center space-x-1">
                  <div className="bg-green-300 rounded-full h-2 w-2"></div>
                  <span className="text-sm">Online agora</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span className="text-sm">Resp. rápida</span>
                </div>
              </div>
            </div>

            {/* Botões */}
            <div className="flex items-center space-x-2">
              <button
                onClick={handleWhatsAppClick}
                className="bg-white text-green-600 px-6 py-2 rounded-full font-semibold hover:bg-green-50 transition-colors duration-200 transform hover:scale-105 shadow-lg"
              >
                Chamar no WhatsApp
              </button>
              
              <button
                onClick={handleDismiss}
                className="text-green-100 hover:text-white p-2 rounded-full hover:bg-green-600 transition-colors duration-200"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Versão mobile simplificada
export const WhatsAppBannerMobile = () => {
  const [isVisible, setIsVisible] = useState(false);
  const whatsappNumber = "5519971636969"; // Número real do cliente

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handleClick = () => {
    const message = "Olá! Vim do site da 3D Stuff 🎯";
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="md:hidden fixed bottom-20 left-4 right-4 z-50 animate-slide-up">
      <div className="bg-green-500 text-white p-3 rounded-2xl shadow-xl flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <MessageCircle className="h-6 w-6" />
          <div>
            <p className="font-semibold text-sm">Dúvidas?</p>
            <p className="text-xs text-green-100">Fale no WhatsApp</p>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <button
            onClick={handleClick}
            className="bg-white text-green-600 px-4 py-1 rounded-full text-sm font-semibold"
          >
            Chamar
          </button>
          <button
            onClick={() => setIsVisible(false)}
            className="text-green-200 hover:text-white"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};