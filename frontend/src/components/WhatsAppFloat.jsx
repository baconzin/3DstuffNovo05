import React, { useState, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';

export const WhatsAppFloat = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  const whatsappNumber = "5519971636969"; // Número real do cliente

  useEffect(() => {
    // Mostrar o botão após 2 segundos para dar tempo da página carregar
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleWhatsAppClick = () => {
    const currentHour = new Date().getHours();
    const isBusinessHours = currentHour >= 8 && currentHour <= 22;
    
    let message = "Olá! 👋 Visitei o site da 3D Stuff e gostaria de conversar sobre os produtos de impressão 3D.";
    
    if (!isBusinessHours) {
      message += "\n\n⏰ Sei que não é horário comercial, mas quando possível, me ajudem por favor!";
    }

    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  const handleMouseEnter = () => {
    setShowTooltip(true);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  if (!isVisible) return null;

  return (
    <>
      {/* Botão Principal do WhatsApp */}
      <div
        className={`fixed bottom-6 right-6 z-50 transition-all duration-300 transform ${
          isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'
        }`}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {/* Tooltip */}
        {showTooltip && (
          <div className="absolute bottom-16 right-0 mb-2 bg-gray-900 text-white px-4 py-2 rounded-lg shadow-lg text-sm whitespace-nowrap animate-fade-in">
            💬 Fale conosco no WhatsApp
            <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
          </div>
        )}

        {/* Botão WhatsApp */}
        <button
          onClick={handleWhatsAppClick}
          className="group relative bg-green-500 hover:bg-green-600 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110 focus:outline-none focus:ring-4 focus:ring-green-300"
        >
          {/* Animação de pulso */}
          <div className="absolute inset-0 bg-green-500 rounded-full animate-ping opacity-20"></div>
          
          {/* Ícone do WhatsApp */}
          <MessageCircle className="h-6 w-6 relative z-10" />
          
          {/* Badge de notificação (opcional) */}
          <div className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold animate-bounce">
            1
          </div>
        </button>
      </div>

      {/* Versão Mobile - Menor e mais discreta */}
      <style jsx>{`
        @media (max-width: 768px) {
          .whatsapp-mobile {
            width: 56px !important;
            height: 56px !important;
          }
        }
      `}</style>
    </>
  );
};

// Componente alternativo mais simples (se preferir)
export const WhatsAppSimple = () => {
  const whatsappNumber = "5519971636969";

  const handleClick = () => {
    const message = "Olá! Vim do site da 3D Stuff e quero saber mais sobre os produtos! 🎯";
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button
        onClick={handleClick}
        className="bg-green-500 hover:bg-green-600 text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        title="Falar no WhatsApp"
      >
        <MessageCircle className="h-6 w-6" />
      </button>
    </div>
  );
};

// Componente com ícone personalizado do WhatsApp (mais realista)
export const WhatsAppCustomIcon = () => {
  const whatsappNumber = "5519971636969";

  const handleClick = () => {
    const message = "Olá! 👋 Estou interessado nos produtos da 3D Stuff. Podem me ajudar?";
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={handleClick}
        className="group bg-green-500 hover:bg-green-600 text-white p-4 rounded-full shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-110 focus:outline-none focus:ring-4 focus:ring-green-300"
        title="💬 Chamar no WhatsApp"
      >
        {/* Ícone WhatsApp SVG mais realista */}
        <svg 
          className="h-7 w-7" 
          fill="currentColor" 
          viewBox="0 0 24 24"
        >
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.309"/>
        </svg>

        {/* Indicador online */}
        <div className="absolute -top-1 -right-1 bg-green-400 rounded-full h-4 w-4 border-2 border-white animate-pulse"></div>
      </button>
    </div>
  );
};