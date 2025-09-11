import React from 'react';
import { Button } from './ui/button';
import { ArrowRight, Zap, Star, Users } from 'lucide-react';
import { companyInfo } from '../mock';

export const Hero = () => {
  const scrollToProducts = () => {
    const element = document.getElementById('products');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="home" className="pt-20 pb-16 bg-gradient-to-br from-gray-50 to-white min-h-screen flex items-center">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-4xl mx-auto">
          {/* Main Title */}
          <div className="mb-8 animate-fade-in">
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              <span className="text-orange-500">3D</span> Stuff
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
              {companyInfo.slogan}
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button 
              onClick={scrollToProducts}
              size="lg"
              className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 text-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              Confira nossos produtos
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button 
              variant="outline"
              size="lg"
              onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
              className="border-2 border-gray-300 text-gray-700 px-8 py-4 text-lg hover:border-orange-500 hover:text-orange-500 transition-all duration-200"
            >
              Sobre nós
            </Button>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="text-center p-6 rounded-2xl bg-white shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-orange-500" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Tecnologia Avançada</h3>
              <p className="text-gray-600">Impressoras 3D de última geração para qualidade superior</p>
            </div>

            <div className="text-center p-6 rounded-2xl bg-white shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-orange-500" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Qualidade Premium</h3>
              <p className="text-gray-600">Materiais de alta qualidade e acabamento impecável</p>
            </div>

            <div className="text-center p-6 rounded-2xl bg-white shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-1">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-orange-500" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Personalização</h3>
              <p className="text-gray-600">Produtos únicos feitos sob medida para você</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};