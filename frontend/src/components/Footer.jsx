import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { ShoppingBag, Instagram, Facebook, Music } from 'lucide-react';
import { companyAPI } from '../services/api';

export const Footer = () => {
  const [companyInfo, setCompanyInfo] = useState(null);

  useEffect(() => {
    loadCompanyInfo();
  }, []);

  const loadCompanyInfo = async () => {
    try {
      const data = await companyAPI.getInfo();
      setCompanyInfo(data);
    } catch (error) {
      console.error('Erro ao carregar informações da empresa:', error);
      // Fallback para dados padrão
      setCompanyInfo({
        name: "3D Stuff",
        email: "contato@3dstuff.com.br",
        social_media: {
          instagram: "@3dstuff",
          facebook: "3DStuff",
          tiktok: "@3dstuff"
        }
      });
    }
  };
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSocialClick = (platform) => {
    // Mock dos links das redes sociais - será implementado com links reais
    const urls = {
      instagram: `https://instagram.com/${companyInfo?.social_media?.instagram || '@3dstuff'}`,
      facebook: `https://facebook.com/${companyInfo?.social_media?.facebook || '3DStuff'}`,
      tiktok: `https://tiktok.com/${companyInfo?.social_media?.tiktok || '@3dstuff'}`
    };
    
    if (urls[platform]) {
      window.open(urls[platform], '_blank');
    }
  };

  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <ShoppingBag className="h-8 w-8 text-orange-500" />
              <span className="text-2xl font-bold">3D Stuff</span>
            </div>
            <p className="text-gray-300 leading-relaxed">
              Transformamos ideias em realidade através da impressão 3D. 
              Produtos únicos e personalizados para você.
            </p>
            <div className="flex space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSocialClick('instagram')}
                className="p-2 hover:bg-gray-800 hover:text-orange-500 transition-colors"
              >
                <Instagram className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSocialClick('facebook')}
                className="p-2 hover:bg-gray-800 hover:text-orange-500 transition-colors"
              >
                <Facebook className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSocialClick('tiktok')}
                className="p-2 hover:bg-gray-800 hover:text-orange-500 transition-colors"
              >
                <Music className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Links Rápidos</h3>
            <div className="space-y-2">
              <button 
                onClick={() => scrollToSection('home')}
                className="block text-gray-300 hover:text-orange-500 transition-colors"
              >
                Início
              </button>
              <button 
                onClick={() => scrollToSection('products')}
                className="block text-gray-300 hover:text-orange-500 transition-colors"
              >
                Produtos
              </button>
              <button 
                onClick={() => scrollToSection('about')}
                className="block text-gray-300 hover:text-orange-500 transition-colors"
              >
                Sobre
              </button>
              <button 
                onClick={() => scrollToSection('contact')}
                className="block text-gray-300 hover:text-orange-500 transition-colors"
              >
                Contato
              </button>
            </div>
          </div>

          {/* Products */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Produtos</h3>
            <div className="space-y-2 text-gray-300">
              <p className="hover:text-orange-500 transition-colors cursor-pointer">Miniaturas</p>
              <p className="hover:text-orange-500 transition-colors cursor-pointer">Utilitários</p>
              <p className="hover:text-orange-500 transition-colors cursor-pointer">Decoração</p>
              <p className="hover:text-orange-500 transition-colors cursor-pointer">Personalizados</p>
            </div>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contato</h3>
            <div className="space-y-2 text-gray-300">
              <p>📧 {companyInfo?.email || "contato@3dstuff.com.br"}</p>
              <p>📱 +55 (11) 99999-9999</p>
              <p>📍 São Paulo, SP - Brasil</p>
            </div>
          </div>
        </div>

        <Separator className="my-8 bg-gray-700" />

        {/* Bottom Bar */}
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="text-gray-400 text-sm">
            © 2025 3D Stuff. Todos os direitos reservados.
          </div>
          <div className="flex space-x-6 text-sm text-gray-400">
            <a href="#" className="hover:text-orange-500 transition-colors">
              Política de Privacidade
            </a>
            <a href="#" className="hover:text-orange-500 transition-colors">
              Termos de Uso
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};